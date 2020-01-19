from azure.cosmosdb.table import Entity
from flask_restful import Resource, reqparse
from flask import jsonify, request
from Settings import Salt
from TableStorage.TableStorageConnection import AzureTableStorage
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, verify_jwt_in_request)
import json

parser = reqparse.RequestParser()
parser.add_argument('Name', type=str, required=False)
parser.add_argument('Datavalue', type=str, required=False)
parser.add_argument('ConnectionString', type=str, required=False)


class SensorData(Resource):
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "OwnerId eq '{0}'".format(get_jwt_claims()["id"])
        rows = table_service.query_entities('sensordata', filter=filter)
        for row in rows:
            row["Timestamp"] = row["Timestamp"].isoformat()
        return {"message": "success", "sensordata": list(rows), "uri": request.base_url}

    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        filter = "PartitionKey eq 'sensordata'"
        sensordata_table = table_service.query_entities('rulers', filter=filter)
        sensordata_table = list(sensordata_table)[0]

        sensors_fields = {
            "PartitionKey": args["ConnectionString"].replace("'", ";"),
            "RowKey": str(sensordata_table["NewId"]),
            "Datavalue": args["Datavalue"].replace("'", ";"),
            "OwnerId": get_jwt_claims()["id"]
        }

        print(sensors_fields)

        table_service.insert_entity('sensors', sensors_fields)
        ruler_sensors = {"PartitionKey": sensordata_table['PartitionKey'], "RowKey": sensordata_table['RowKey'],
                         "NewId": sensordata_table["NewId"] + 1, "Size": sensordata_table["Size"] + 1}
        print(ruler_sensors)
        table_service.update_entity('rulers', ruler_sensors)

        return {"message": "success", "sensordata": sensors_fields}

class SingleSensorData(Resource):
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
            return {"message": "error id not found"}

        filter = "OwnerId eq '{0}' and {1} eq '{2}'".format(get_jwt_claims()["id"], searcher, specification)

        sensordata = table_service.query_entities('sensordata', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error data not found"}

        sensordata["Timestamp"] = sensordata["Timestamp"].isoformat()
        return {"message": "success", "sensordata": sensordata, "uri": request.base_url}

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

        sensordata = table_service.query_entities('sensordata', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error device not found"}

        sensordata["PartitionKey"] = args["ConnectionString"].replace("'", ";")
        sensordata["Name"] = args["Name"].replace("'", ";")
        sensordata["Datavalue"] = args["Datavalue"].replace("'", ";")
        del sensordata["etag"]

        table_service.update_entity('sensordata', sensordata)

        sensordata["Timestamp"] = sensordata["Timestamp"].isoformat()
        return {"message": "success", "sensordata": sensordata, "uri": request.base_url}

    @jwt_required
    def delete(self, id):
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

        sensordata = table_service.query_entities('sensordata', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error device not found"}

        table_service.delete_entity('sensordata', sensordata["PartitionKey"], sensordata["RowKey"])

        return {"message": "success deleted sensordata {}".format(sensordata["Name"])}
