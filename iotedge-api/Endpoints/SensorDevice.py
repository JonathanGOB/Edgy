from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify, request

from Helpers.Cascade import Cascade
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)
import json

parser = reqparse.RequestParser()
parser.add_argument('EdgeDeviceId', type=str, required=False)
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Location', type=str, required=False)
parser.add_argument('Description', type=str, required=False)
parser.add_argument('Protocol', type=str, required=False)


class SensorsDevices(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "OwnerId eq '{0}'".format(get_jwt_claims()["id"])
        rows = table_service.query_entities('sensorsdevices', filter=filter)
        for row in rows:
            row["Timestamp"] = row["Timestamp"].isoformat()
        return {"message": "success", "sensorsdevices": list(rows), "uri": request.base_url}

    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        filter = "PartitionKey eq 'sensorsdevices'"
        sensorsdevices_table = table_service.query_entities('rulers', filter=filter)
        sensorsdevices_table = list(sensorsdevices_table)[0]

        sensordevices_fields = {
            "PartitionKey": args["Location"].replace("'", ";"),
            "RowKey": str(sensorsdevices_table["NewId"]),
            "Name": args["Name"].replace("'", ";"),
            "Description": args["Description"].replace("'", ";"),
            "Protocol": args["Protocol"].replace("'", ";"),
            "EdgeDeviceId": args["EdgeDeviceId"].replace("'", ";"),
            "OwnerId": get_jwt_claims()["id"]
        }

        print(sensordevices_fields)

        check = "Name eq '{}' and EdgeDeviceId eq '{}'".format(args["Name"].replace("'", ";"), args["EdgeDeviceId"].replace("'", ";"))

        check_sensorsdevices = table_service.query_entities(
            'sensorsdevices', filter=check)

        if len(list(check_sensorsdevices)) >= 1:
            return {"message": "error duplicate name"}

        table_service.insert_entity('sensorsdevices', sensordevices_fields)
        ruler_sensordevices = {"PartitionKey": sensorsdevices_table['PartitionKey'], "RowKey": sensorsdevices_table['RowKey'],
                             "NewId": sensorsdevices_table["NewId"] + 1, "Size": sensorsdevices_table["Size"] + 1}
        print(ruler_sensordevices)
        table_service.update_entity('rulers', ruler_sensordevices)

        return {"message": "success", "sensorsdevice": sensordevices_fields}


class SingleSensorsDevice(Resource):
    @jwt_required
    def get(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        specification = None
        searcher = None

        if id:
            specification = id
            searcher = "RowKey"

        else:
            return {"message": "error device not found"}

        filter = "OwnerId eq '{0}' and {1} eq '{2}'".format(get_jwt_claims()["id"], searcher, specification)

        sensordevices = table_service.query_entities('sensorsdevices', filter=filter)
        if len(list(sensordevices)) > 0:
            sensordevices = list(sensordevices)[0]
        else:
            return {"message": "error device not found"}

        sensordevices["Timestamp"] = sensordevices["Timestamp"].isoformat()
        return {"message": "success", "sensorsdevice": sensordevices, "uri": request.base_url}


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

        sensorsdevice = table_service.query_entities('sensorsdevices', filter=filter)
        if len(list(sensorsdevice)) > 0:
            sensorsdevice = list(sensorsdevice)[0]
        else:
            return {"message": "error device not found"}

        sensorsdevice["EdgeDeviceId"] = args["EdgeDeviceId"].replace("'", ";")
        sensorsdevice["Name"] = args["Name"].replace("'", ";")
        sensorsdevice["PartitionKey"] = args["Location"].replace("'", ";")
        sensorsdevice["Description"] = args["Description"].replace("'", ";")
        sensorsdevice["Protocol"] = args["Protocol"].replace("'", ";")
        del sensorsdevice["etag"]

        table_service.update_entity('sensorsdevices', sensorsdevice)

        sensorsdevice["Timestamp"] = sensorsdevice["Timestamp"].isoformat()
        return {"message": "success", "sensorsdevice": sensorsdevice, "uri": request.base_url}

    @jwt_required
    def delete(self, id):
        storage = AzureTableStorage()
        verify_jwt_in_request()

        master_list = [["EdgeDeviceId", "SensorsDeviceId", "ConnectionString"],
                       ["sensorsdevices", "sensors", "sensordata"]]
        cascader = Cascade(get_jwt_claims(), id, master_list)
        sensorsdevice = cascader.delete()
        if sensorsdevice == None:
            return {"message": "device not found"}
        return {"message": "success deleted sensordevice {}".format(sensorsdevice["Name"])}

class GetEdgeSensorsDevices(Resource):
    @jwt_required
    def get(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()

        filter = "OwnerId eq '{0}' and EdgeDeviceId eq '{1}'".format(get_jwt_claims()["id"], id.replace("'", ";"))

        sensorsdevices = table_service.query_entities('sensorsdevices', filter=filter)
        print(list(sensorsdevices))
        if len(list(sensorsdevices)) > 0:
            sensorsdevices = list(sensorsdevices)
        else:
            return {"message": "error device not found"}

        for sensorsdevice in sensorsdevices:
            sensorsdevice["Timestamp"] = sensorsdevice["Timestamp"].isoformat()

        return {"message": "success", "sensorsdevices": list(sensorsdevices), "uri": request.base_url}
