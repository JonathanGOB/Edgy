from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify, request
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)
import json
import hashlib

parser = reqparse.RequestParser()
parser.add_argument('SensorsDeviceId', type=str, required=False)
parser.add_argument('Location', type=str, required=False)
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Datatype', type=str, required=False)
parser.add_argument('Description', type=str, required=False)


class Sensors(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "OwnerId eq '{0}'".format(get_jwt_claims()["id"])
        rows = table_service.query_entities('sensors', filter=filter)
        for row in rows:
            row["Timestamp"] = row["Timestamp"].isoformat()
        return {"message": "success", "sensors": list(rows), "uri": request.base_url}

    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        filter = "PartitionKey eq 'sensors'"
        sensors_table = table_service.query_entities('rulers', filter=filter)
        sensors_table = list(sensors_table)[0]

        sensors_fields = {
            "PartitionKey": args["Location"].replace("'", ";"),
            "RowKey": str(sensors_table["NewId"]),
            "Name": args["Name"].replace("'", ";"),
            "Description": args["Description"].replace("'", ";"),
            "SensorsDeviceId": args["SensorsDeviceId"].replace("'", ";"),
            "ConnectionString": hashlib.sha256((args["Location"].replace("'", ";").encode('utf-8') + str(sensors_table["NewId"]).encode('utf-8'))).hexdigest(),
            "Datatype": args["Datatype"].replace("'", ";"),
            "OwnerId": get_jwt_claims()["id"]
        }

        print(sensors_fields)

        check = "Name eq '{}'".format(args["Name"].replace("'", ";"))

        check_sensors = table_service.query_entities(
            'sensors', filter=check)

        if len(list(check_sensors)) >= 1:
            return {"message": "error duplicate name"}

        table_service.insert_entity('sensors', sensors_fields)
        ruler_sensors = {"PartitionKey": sensors_table['PartitionKey'], "RowKey": sensors_table['RowKey'],
                             "NewId": sensors_table["NewId"] + 1, "Size": sensors_table["Size"] + 1}
        print(ruler_sensors)
        table_service.update_entity('rulers', ruler_sensors)

        return {"message": "success", "sensors": sensors_fields}


class GetSingleSensor(Resource):
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

        sensors = table_service.query_entities('sensors', filter=filter)
        if len(list(sensors)) > 0:
            sensors = list(sensors)[0]
        else:
            return {"message": "error device not found"}

        return {"message": "success", "sensors": list(sensors), "uri": request.base_url}

