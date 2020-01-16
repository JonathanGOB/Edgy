from flask_restful import Api, Resource, reqparse, fields, marshal
from datetime import datetime
from TableStorageConnection import AzureTableStorage

deviceData_fields = {
    'PartitionKey': fields.String,
    'RowKey': fields.Integer,
    'Name': fields.String,
    'Email': fields.String,
    'Password': fields.String,
    'timestamp': fields.DateTime,
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
        self.reqparse.add_argument('timestamp', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
                                   required=False)
        super(User, self).__init__()

    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        filter = "PartitionKey eq 'Groningen'and Timestamp lt datetime'{}'".format(datetime.utcnow().isoformat())
        print(filter)
        rows = table_service.query_entities('users', filter=filter)
        for row in rows:
            print(row)
