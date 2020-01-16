from flask_restful import Api, Resource, reqparse, fields, marshal
from datetime import datetime
from TableStorageConnection import AzureTableStorage

User_fields = {
    'PartitionKey': fields.String,
    'RowKey': fields.Integer,
    'Name': fields.String,
    'Email': fields.String,
    'Password': fields.String,
    'uri': fields.Url('User')
}

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('PartitionKey', type=str, required=False)
        self.reqparse.add_argument('RowKey', type=int, required=False)
        self.reqparse.add_argument('Name', type=str, required=False)
        self.reqparse.add_argument('Email', type=str, required=False)
        self.reqparse.add_argument('Password', type=str, required=False)
        self.reqparse.add_argument('Password', type=str, required=False)
        self.reqparser.add_argument('Authorization', type=str, location='headers', required=False)
        super(User, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        filter = "Name eq '{}'".format(args['Name'])
        

    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        rows = table_service.query_entities('users')
        rows = list(rows)
        latest_user = rows[len(rows) - 1]
        NewRowKey = int(latest_user['RowKey']) + 1

