from flask_restful import Api, Resource, reqparse, fields, marshal
from datetime import datetime
from TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


parser = reqparse.RequestParser()
parser.add_argument('PartitionKey', type=str, required=False)
parser.add_argument('RowKey', type=int, required=False)
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Email', type=str, required=False)
parser.add_argument('Password', type=str, required=False)

class UserLogin(Resource):
    def get(self):
        args = self.reqparse.parse_args()
        filter = "Name eq '{}'".format(args['Name'])


class UserRegistration(Resource):
    def post(self):
        args = self.reqparse.parse_args()

        storage = AzureTableStorage()
        table_service = storage.get_table()
        rows = table_service.query_entities('users')
        rows = list(rows)
        NewRowKey = None

        if rows:
            latest_user = rows[len(rows) - 1]
            print(latest_user)
            NewRowKey = int(latest_user['RowKey']) + 1

        if not rows:
            NewRowKey = 0


        user = Entity()
        user.PartitionKey = 'Admin'
        user.RowKey = NewRowKey
        user.Name =  args['Name']
        user.Password = bcrypt.hashpw(base64.b64encode(args["Password"].encode("utf-8")), Salt.salt)
        user.Email = args['Email']

        print(user)

        check = "Email eq '{}'".format(args["Email"])

        check_user = table_service.query_entities(
            'users', filter=check)

        if len(list(check_user)) >= 1:
            return {"Message":"Error user already exists"}

        table_service.insert_entity('users', user)
        return {"message": "success", "user": user}


