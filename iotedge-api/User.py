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
        storage = AzureTableStorage()
        table_service = storage.get_table()
        rows = table_service.query_entities('users')
        rows = list(rows)
        latest_user = rows[len(rows) - 1]
        NewRowKey = int(latest_user['RowKey']) + 1

