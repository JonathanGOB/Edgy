from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify, request

from Helpers.Cascade import Cascade
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)
import json

# Get data from the url
parser = reqparse.RequestParser()
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Location', type=str, required=False)
parser.add_argument('Description', type=str, required=False)


class EdgeDevices(Resource):

    # Get all edgedevices of the owner
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "OwnerId eq '{0}'".format(get_jwt_claims()["id"])
        rows = table_service.query_entities('edgedevices', filter=filter)
        for row in rows:
            row["Timestamp"] = row["Timestamp"].isoformat()
        return {"message": "success", "data": {"edgedevices": list(rows), "uri": request.base_url}}, 200

    # Make new EdgeDevice
    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        isNew = False
        while not isNew:
            try:
                filter = "PartitionKey eq 'edgedevices'"
                edgedevice_table = table_service.query_entities('rulers', filter=filter)
                edgedevice_table = list(edgedevice_table)[0]
                ruler_edgedevices = {"PartitionKey": edgedevice_table['PartitionKey'],
                                     "RowKey": edgedevice_table['RowKey'],
                                     "NewId": edgedevice_table["NewId"] + 1, "Size": edgedevice_table["Size"] + 1}
                table_service.update_entity('rulers', ruler_edgedevices, if_match=edgedevice_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        try:
            edgedevice_fields = {
                "PartitionKey": args["Location"].replace("'", ";"),
                "RowKey": str(edgedevice_table["NewId"]),
                "Name": args["Name"].replace("'", ";"),
                "Description": args["Description"].replace("'", ";"),
                "OwnerId": get_jwt_claims()["id"]
            }

        except:
            return {"message": "not everything filled"}, 400

        check = "Name eq '{}'".format(args["Name"].replace("'", ";"))

        check_edgedevice = table_service.query_entities(
            'edgedevices', filter=check)

        if len(list(check_edgedevice)) >= 1:
            return {"message": "error duplicate name"}, 400

        table_service.insert_entity('edgedevices', edgedevice_fields)

        return {"message": "success", "data": {"edgedevice": edgedevice_fields}}, 200


class SingleEdgeDevice(Resource):

    # Get EdgeDevice by id(RowKey)
    @jwt_required
    def get(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        specification = None
        searcher = None

        if id:
            specification = id.replace("'", ";")
            searcher = "RowKey"

        else:
            return {"message": "error device not found"}, 400

        filter = "OwnerId eq '{0}' and {1} eq '{2}'".format(get_jwt_claims()["id"], searcher, specification)

        edgedevice = table_service.query_entities('edgedevices', filter=filter)
        if len(list(edgedevice)) > 0:
            edgedevice = list(edgedevice)[0]
        else:
            return {"message": "error device not found"}, 400

        edgedevice["Timestamp"] = edgedevice["Timestamp"].isoformat()
        return {"message": "success", "data": {"edgedevice": edgedevice, "uri": request.base_url}}, 200

    # Update EdgeDevice by id
    @jwt_required
    def put(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        specification = None
        searcher = None

        if id:
            specification = id.replace("'", ";")
            searcher = "RowKey"

        else:
            return {"message": "error device not found"}

        filter = "OwnerId eq '{0}' and {1} eq '{2}'".format(get_jwt_claims()["id"], searcher, specification)

        edgedevice = table_service.query_entities('edgedevices', filter=filter)
        if len(list(edgedevice)) > 0:
            edgedevice = list(edgedevice)[0]
        else:
            return {"message": "error device not found"}

        try:
            edgedevice["Name"] = args["Name"].replace("'", ";")
            edgedevice["PartitionKey"] = args["Location"].replace("'", ";")
            edgedevice["Description"] = args["Description"].replace("'", ";")
            del edgedevice["etag"]
        except:
            return {"message": "fill all data"}, 400
        table_service.update_entity('edgedevices', edgedevice)

        edgedevice["Timestamp"] = edgedevice["Timestamp"].isoformat()
        return {"message": "success", "data": {"edgedevice": edgedevice, "uri": request.base_url}}, 200

    # Delete EdgeDevice by id and all the children of the EdgeDevice
    @jwt_required
    def delete(self, id):
        storage = AzureTableStorage()
        verify_jwt_in_request()
        table_service = AzureTableStorage().get_table()

        isNew = False
        while not isNew:
            try:
                filter = "PartitionKey eq 'edgedevices'"
                edgedevice_table = table_service.query_entities('rulers', filter=filter)
                edgedevice_table = list(edgedevice_table)[0]
                ruler_edgedevices = {"PartitionKey": edgedevice_table['PartitionKey'],
                                     "RowKey": edgedevice_table['RowKey'],
                                     "NewId": edgedevice_table["NewId"], "Size": edgedevice_table["Size"] - 1}
                table_service.update_entity('rulers', ruler_edgedevices, if_match=edgedevice_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        master_list = [["", "EdgeDeviceId", "SensorsDeviceId", "ConnectionString"],
                       ["edgedevices", "sensorsdevices", "sensors", "sensordata"]]
        cascader = Cascade(get_jwt_claims(), id, master_list)
        edgedevice = cascader.delete()
        if edgedevice == None:
            return {"message": "device not found"}, 400
        return {"message": "success deleted edgedevice {}".format(edgedevice["Name"])}, 200
