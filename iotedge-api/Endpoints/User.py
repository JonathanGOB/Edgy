import base64
import bcrypt
from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)


parser = reqparse.RequestParser()
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Email', type=str, required=False)
parser.add_argument('Password', type=str, required=False)

class UserObject:
    def __init__(self, username, email, id):
        self.username = username
        self.email = email
        self.id = id

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class UserLogin(Resource):
    def get(self):
        args = parser.parse_args()
        storage = AzureTableStorage()
        table_service = storage.get_table()
        filter = "Email eq '{}'".format(args['Email'])
        user = table_service.query_entities('users', filter=filter)
        user = list(user)[0]

        if not user:
            return {"message": "email {} doesn't exist".format(args['Email'])}
        if user:
            if bcrypt.checkpw(args['Password'].encode("utf-8"), user['Password'].encode("utf-8")):
                try:
                    userObject = UserObject(username=user["Name"], email=user["Email"], id=user["RowKey"])
                    access_token = create_access_token(identity = userObject)
                    refresh_token = create_refresh_token(identity = userObject)

                    return {
                        'message': 'Logged in as {}'.format(user['Name']),
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                except Exception as e:
                    print(e)
                    return {"message" : "something went wrong"}
            else:
                return {"message": "wrong password"}


class UserRegistration(Resource):
    def post(self):
        args = parser.parse_args()

        storage = AzureTableStorage()
        table_service = storage.get_table()
        filter = "PartitionKey eq 'users'"
        user_table = table_service.query_entities('rulers', filter=filter)
        user_table = list(user_table)[0]
        print(user_table)

        user = Entity()
        user.PartitionKey = 'user'
        user.RowKey = str(user_table['NewId'])
        user.Name =  args['Name']
        user.Password = (bcrypt.hashpw(args["Password"].encode("utf-8"), Salt.salt)).decode('utf-8')
        user.Email = args['Email']

        print(user)

        check = "Email eq '{}'".format(args["Email"])

        check_user = table_service.query_entities(
            'users', filter=check)

        if len(list(check_user)) >= 1:
            return {"message": "error email already used"}

        table_service.insert_entity('users', user)
        ruler_users = {"PartitionKey": user_table['PartitionKey'], "RowKey": user_table['RowKey'], "NewId": user_table["NewId"] + 1, "Size": user_table["Size"] + 1}
        table_service.update_entity('rulers', ruler_users)
        user.Password = args["Password"]
        return {"message": "success", "user": user}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        jti = get_raw_jwt()['jti']
        filter = "PartitionKey eq 'revokedtokens'"
        revokedtokens_table = table_service.query_entities('revokedtokens', filter=filter)
        revokedtokens_table = list(revokedtokens_table)[0]

        try:
            revoked_token = {"PartitionKey": "AccessToken", "RowKey": revokedtokens_table["NewId"], "Token": jti}
            ruler_revokedtokens = {"PartitionKey": revokedtokens_table['PartitionKey'],
                                   "RowKey": revokedtokens_table['RowKey'],
                                   "NewId": revokedtokens_table["NewId"] + 1, "Size": revokedtokens_table["Size"] + 1}
            table_service.update_entity('rulers', ruler_revokedtokens)
            table_service.insert_entity(revoked_token)
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        jti = get_raw_jwt()['jti']
        filter = "PartitionKey eq 'revokedtokens'"
        revokedtokens_table = table_service.query_entities('revokedtokens', filter=filter)
        revokedtokens_table = list(revokedtokens_table)[0]

        try:
            revoked_token = {"PartitionKey": "RefreshToken", "RowKey": revokedtokens_table["NewId"], "Token": jti}
            ruler_revokedtokens = {"PartitionKey": revokedtokens_table['PartitionKey'], "RowKey": revokedtokens_table['RowKey'],
                           "NewId": revokedtokens_table["NewId"] + 1, "Size": revokedtokens_table["Size"] + 1}
            table_service.update_entity('rulers', ruler_revokedtokens)
            table_service.insert_entity(revoked_token)
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}

class GetUser(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "Email eq '{}'".format(get_jwt_claims()["email"])
        user = table_service.query_entities('users', filter=filter)
        user = list(user)[0]

        return {"message": "success", "user": user}

