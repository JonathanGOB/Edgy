from flask_restful import Api, Resource, reqparse, fields, marshal
from datetime import datetime
from TableStorageConnection import AzureTableStorage
from azure.cosmosdb.table.models import Entity
import Salt
import bcrypt
import base64


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
        self.reqparse.add_argument('Authorization', type=str, location='headers', required=False)
        super(User, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        filter = "Name eq '{}'".format(args['Name'])
        

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


