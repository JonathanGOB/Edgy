import base64
import datetime

import bcrypt
from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse, fields
from flask import jsonify, request

from Helpers.Cascade import Cascade
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)
import json
import copy

parser = reqparse.RequestParser()
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Email', type=str, required=False)
parser.add_argument('Password', type=str, required=False)
parser.add_argument('NewPassword', type=str, required=False)


class UserObject:
    def __init__(self, username, email, id):
        self.username = username
        self.email = email
        self.id = id


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"data": {'access_token': access_token, "uri": request.base_url}}, 200


class UserLogin(Resource):
    def get(self):
        args = parser.parse_args()
        storage = AzureTableStorage()
        table_service = storage.get_table()
        filter = "Email eq '{}'".format(args['Email'])
        user = table_service.query_entities('users', filter=filter)
        try:
            user = list(user)[0]
        except Exception as e:
            return {"data": {"message": "email {} doesn't exist".format(args['Email'])}}, 400

        if user:
            if bcrypt.checkpw(args['Password'].replace("'", ";").encode("utf-8"), user['Password'].encode("utf-8")):
                try:
                    userObject = UserObject(username=user["Name"], email=user["Email"], id=user["RowKey"])
                    expires = datetime.timedelta(days=1)
                    access_token = create_access_token(identity=userObject, expires_delta=expires)
                    refresh_token = create_refresh_token(identity=userObject)

                    return {
                               "data": {
                                   'message': 'Logged in as {}'.format(user['Name']),
                                   'user': {"name": user['Name'], "email": user['Email'], "id": user['RowKey']},
                                   'access_token': access_token,
                                   'refresh_token': refresh_token,
                                   "uri": request.base_url
                               }
                           }, 200

                except:
                    return {"data": {"message": "something went wrong"}}, 500
            else:
                return {"data": {"message": "wrong password"}}, 400


class UserRegistration(Resource):
    def post(self):
        args = parser.parse_args()

        storage = AzureTableStorage()
        table_service = storage.get_table()
        filter = "PartitionKey eq 'users'"
        isNew = False
        while not isNew:
            try:
                user_table = table_service.query_entities('rulers', filter=filter)
                user_table = list(user_table)[0]
                ruler_users = {"PartitionKey": user_table['PartitionKey'], "RowKey": user_table['RowKey'],
                               "NewId": user_table["NewId"] + 1, "Size": user_table["Size"] + 1}
                table_service.update_entity('rulers', ruler_users, if_match=user_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        try:
            user = Entity()
            user.PartitionKey = 'user'
            user.RowKey = str(user_table['NewId'])
            user.Name = args['Name'].replace("'", ";")
            user.Password = (bcrypt.hashpw(args["Password"].encode("utf-8"), Salt.salt)).decode('utf-8')
            user.Email = args['Email'].replace("'", ";")
            check = "Email eq '{}'".format(args["Email"])

            check_user = table_service.query_entities(
                'users', filter=check)

        except:
            return {"message": "not everything filled"}, 400

        if len(list(check_user)) >= 1:
            return {"message": "error email already used"}, 400

        table_service.insert_entity('users', user)
        user.Password = args["Password"]
        return {"data": {"message": "success", "user": user, "uri": request.base_url}}, 200


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        global revokedtokens_table
        storage = AzureTableStorage()
        table_service = storage.get_table()
        jti = get_raw_jwt()['jti']
        filter = "PartitionKey eq 'revokedtokens'"
        isNew = False
        while not isNew:
            try:
                revokedtokens_table = table_service.query_entities('rulers', filter=filter)
                revokedtokens_table = list(revokedtokens_table)[0]
                ruler_revokedtokens = {"PartitionKey": revokedtokens_table['PartitionKey'],
                                       "RowKey": revokedtokens_table['RowKey'],
                                       "NewId": revokedtokens_table["NewId"] + 1,
                                       "Size": revokedtokens_table["Size"] + 1}
                table_service.update_entity('rulers', ruler_revokedtokens, if_match=revokedtokens_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        try:
            revoked_token = {"PartitionKey": "AccessToken", "RowKey": str(revokedtokens_table["NewId"]), "Token": jti}
            table_service.insert_entity('revokedtokens', revoked_token)
            return {"data": {'message': 'Access token has been revoked', "uri": request.base_url}}, 200
        except:
            return {"data": {'message': 'Something went wrong'}}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        jti = get_raw_jwt()['jti']
        filter = "PartitionKey eq 'revokedtokens'"

        isNew = False
        while not isNew:
            try:
                revokedtokens_table = table_service.query_entities('revokedtokens', filter=filter)
                revokedtokens_table = list(revokedtokens_table)[0]
                ruler_revokedtokens = {"PartitionKey": revokedtokens_table['PartitionKey'],
                                       "RowKey": revokedtokens_table['RowKey'],
                                       "NewId": revokedtokens_table["NewId"] + 1,
                                       "Size": revokedtokens_table["Size"] + 1}
                table_service.update_entity('rulers', ruler_revokedtokens, if_match=revokedtokens_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        try:
            revoked_token = {"PartitionKey": "RefreshToken", "RowKey": revokedtokens_table["NewId"], "Token": jti}
            table_service.insert_entity('revokedtokens', revoked_token)
            return {"data": {'message': 'Access token has been revoked', "uri": request.base_url}}, 200
        except:
            return {"data": {'message': 'Something went wrong'}}, 500


class Account(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "RowKey eq '{}'".format(get_jwt_claims()["id"])
        user = table_service.query_entities('users', filter=filter)
        user = list(user)[0]
        timestamp = user["Timestamp"].isoformat()
        return {"data": {"message": "success",
                         "user": {"name": user["Name"], "email": user["Email"], "id": user["RowKey"]},
                         "Last_updated": timestamp,
                         "uri": request.base_url}}, 200

    @jwt_required
    def put(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "RowKey eq '{}'".format(get_jwt_claims()["id"])
        user = table_service.query_entities('users', filter=filter)
        user = list(user)[0]

        args = parser.parse_args()

        if bcrypt.checkpw(args['Password'].encode("utf-8"), user['Password'].encode("utf-8")):
            try:
                copy_user = copy.deepcopy(user)

                user["Name"] = args["Name"].replace("'", ";")
                user["Email"] = args["Email"].replace("'", ";")
                user["Password"] = (
                    bcrypt.hashpw(args["NewPassword"].replace("'", ";").encode("utf-8"), Salt.salt)).decode('utf-8')
                del user["etag"]

                print(user)
                print(args)
                filter = "Email eq '{0}' and Email ne '{1}'".format(args["Email"].replace("'", ";"), copy_user["Email"])

                checker = table_service.query_entities('users', filter)
                if len(list(checker)) > 0:
                    return {"data": {"message": "email already used"}}, 400

                elif len(list(checker)) == 0:
                    table_service.delete_entity('users', copy_user["PartitionKey"], copy_user["RowKey"])
                    table_service.insert_entity('users', user)
                    user["Timestamp"] = user["Timestamp"].isoformat()
                    return {"data": {"message": "succes", "data": {"user": user, "uri": request.base_url}}}, 200
            except:
                return {"data": {"message": "not everything  filled"}}, 400

        return {"data": {"message": "wrong password", "uri": request.base_url}}, 400

    def delete(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "RowKey eq '{}'".format(get_jwt_claims()["id"])
        user = table_service.query_entities('users', filter=filter)
        user = list(user)[0]

        args = parser.parse_args()
        if args['Password'] and bcrypt.checkpw(args['Password'].encode("utf-8"), user['Password'].encode("utf-8")):
            isNew = False
            while not isNew:
                try:
                    filter = "PartitionKey eq 'users'"
                    user_table = table_service.query_entities('rulers', filter=filter)
                    user_table = list(user_table)[0]
                    ruler_users = {"PartitionKey": user_table['PartitionKey'], "RowKey": user_table['RowKey'],
                                   "NewId": user_table["NewId"], "Size": user_table["Size"] - 1}
                    table_service.update_entity('rulers', ruler_users, if_match=user_table["etag"])
                    isNew = True
                except:
                    print("concurrency problems")

            master_list = [["", "EdgeDeviceId", "SensorsDeviceId", "ConnectionString"],
                           ["edgedevices", "sensorsdevices", "sensors", "sensordata"]]

            filter = "OwnerId eq '{}'".format(get_jwt_claims()["id"])
            rows = table_service.query_entities('edgedevices', filter=filter)
            for row in rows:
                cascader = Cascade(get_jwt_claims(), row["RowKey"], master_list)
                edgedevice = cascader.delete()
                if edgedevice == None:
                    return {"message": "something went wrong"}, 500

            table_service.delete_entity('users', user["PartitionKey"], user["RowKey"])
            return {"data": {"message": "succes deleted user {}".format(user["Name"]), "uri": request.base_url}}, 200

        return {"data": {"message": "wrong password"}}, 400
