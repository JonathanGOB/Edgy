from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)

parser = reqparse.RequestParser()
parser.add_argument('ForeignKeyUser', type=str, required=False)
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Location', type=str, required=False)
parser.add_argument('Description', type=str, required=False)

class EdgeDevice(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "owner_id eq '{}'".format(get_jwt_claims["email"])
        rows = table_service.query_entities('edgedevices', filter=filter)
