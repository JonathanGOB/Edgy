import base64

import bcrypt
from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage

parser = reqparse.RequestParser()
parser.add_argument('PartitionKey', type=str, required=False)
parser.add_argument('RowKey', type=int, required=False)
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Email', type=str, required=False)
parser.add_argument('Password', type=str, required=False)

class UserLogin(Resource):
    def get(self):
        args = parser.parse_args()
        filter = "Name eq '{}'".format(args['Name'])


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
            return {"Message": "Error email already used"}

        table_service.insert_entity('users', user)
        ruler_users = {"PartitionKey": user_table['PartitionKey'], "RowKey": user_table['RowKey'], "NewId": user_table["NewId"] + 1, "Size": user_table["Size"] + 1}
        table_service.update_entity('rulers', ruler_users)
        user.Password = args["Password"]
        return {"message": "success", "user": user}


