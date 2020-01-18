from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify, request
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)
import json

parser = reqparse.RequestParser()
parser.add_argument('ForeignKeyUser', type=str, required=False)
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Location', type=str, required=False)
parser.add_argument('Description', type=str, required=False)
parser.add_argument('DeviceId', type=int, required=False)


class EdgeDevices(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "owner_id eq '{0}'".format(get_jwt_claims()["id"])
        rows = table_service.query_entities('edgedevices', filter=filter)
        return {"message": "success", "devices": list(rows), "uri": request.base_url}

    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        filter = "PartitionKey eq 'edgedevices'"
        edgedevice_table = table_service.query_entities('rulers', filter=filter)
        edgedevice_table = list(edgedevice_table)[0]

        edgedevice_fields = {
            "PartitionKey": args["Location"],
            "RowKey": edgedevice_table["NewId"],
            "Name": args["Name"],
            "Description": args["Description"],
            "OwnerId": get_jwt_claims()["id"]
        }

        check = "Name eq '{}'".format(args["Name"])

        check_edgedevice = table_service.query_entities(
            'edgedevices', filter=check)

        if len(list(check_edgedevice)) >= 1:
            return {"message": "error duplicate name"}

        table_service.insert_entity('edgedevice', edgedevice_fields)
        ruler_edgedevices = {"PartitionKey": edgedevice_table['PartitionKey'], "RowKey": edgedevice_table['RowKey'],
                             "NewId": edgedevice_table["NewId"] + 1, "Size": edgedevice_table["Size"] + 1}
        table_service.insert_entity('edgedevices', ruler_edgedevices)

        return {"message": "success", "edgedevice": edgedevice_fields}


class GetSingleDevice(Resource):
    @jwt_required
    def get(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        specification = None
        searcher = None

        if not id:
            specification = id
            searcher = "DeviceId"

        else:
            return {"message": "error device not found"}

        filter = "owner_id eq '{0}' and {1} eq '{2}'".format(get_jwt_claims()["id"], searcher, specification)

        edgedevice = table_service.query_entities('edgedevices', filter=filter)
        edgedevice = list(edgedevice)[0]

        return {"message": "success", "devices": list(edgedevice), "uri": request.base_url}

