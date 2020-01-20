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

    #  Get all SensorData by owner
    # @jwt_required
    # def get(self):
    #     storage = AzureTableStorage()
    #     table_service = storage.get_table()
    #     verify_jwt_in_request()
    #     args = parser.parse_args()
    #     filter = "OwnerId eq '{0}' and ConnectionString eq {1}".format(get_jwt_claims()["id"], )
    #     filter = "PartitionKey eq '{0}'".format(args["ConnectionString"])
    #     rows = table_service.query_entities('sensordata', filter=filter)
    #     for row in rows:
    #         row["Timestamp"] = row["Timestamp"].isoformat()
    #     return {"message": "success", "sensordata": list(rows), "uri": request.base_url}, 200

    # Post new SensorData
    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        filter = "PartitionKey eq 'sensordata'"
        sensordata_table = table_service.query_entities('rulers', filter=filter)
        sensordata_table = list(sensordata_table)[0]

        try:
            sensors_fields = {
                "PartitionKey": args["ConnectionString"].replace("'", ";"),
                "RowKey": str(sensordata_table["NewId"]),
                "Datavalue": args["Datavalue"].replace("'", ";"),
            }
        except:
            return {"message": "fill all data"}, 400


        table_service.insert_entity('sensors', sensors_fields)
        ruler_sensors = {"PartitionKey": sensordata_table['PartitionKey'], "RowKey": sensordata_table['RowKey'],
                         "NewId": sensordata_table["NewId"] + 1, "Size": sensordata_table["Size"] + 1}
        table_service.update_entity('rulers', ruler_sensors)

        return {"message": "success", "sensordata": sensors_fields}, 200


class SingleSensorData(Resource):

    # Get SensorData by id
    @jwt_required
    def get(self, partitionkey, id):
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
            return {"message": "error id not found"}, 400

        filter = "PartitionKey eq '{0}' and {1} eq '{2}'".format(partitionkey, searcher, specification)

        sensordata = table_service.query_entities('sensordata', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error data not found"}, 400

        sensordata["Timestamp"] = sensordata["Timestamp"].isoformat()
        return {"message": "success", "sensordata": sensordata, "uri": request.base_url}, 200

    # Update SensorData by id
    @jwt_required
    def put(self, partitionkey, id):
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

        filter = "PartitionKey eq '{0}' and {1} eq '{2}'".format(partitionkey, searcher, specification)

        sensordata = table_service.query_entities('sensordata', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error device not found"}

        try:
            sensordata["PartitionKey"] = args["ConnectionString"].replace("'", ";")
            sensordata["Name"] = args["Name"].replace("'", ";")
            sensordata["Datavalue"] = args["Datavalue"].replace("'", ";")
            del sensordata["etag"]
        except:
            return {"message": "fill data"}, 400

        table_service.update_entity('sensordata', sensordata)

        sensordata["Timestamp"] = sensordata["Timestamp"].isoformat()
        return {"message": "success", "sensordata": sensordata, "uri": request.base_url}, 200

    # Delete SensorData by id
    @jwt_required
    def delete(self, partitionkey, id):
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

        filter = "PartitionKey eq '{0}' and {1} eq '{2}'".format(partitionkey, searcher, specification)

        sensordata = table_service.query_entities('sensordata', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error device not found"}, 400

        table_service.delete_entity('sensordata', sensordata["PartitionKey"], sensordata["RowKey"])

        return {"message": "success deleted sensordata {}".format(sensordata["Name"])}, 200


class GetSensorSensorData(Resource):

    # Get all SensorData from ConnectionString
    @jwt_required
    def get(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()

        filter = "OwnerId eq '{0}' and RowKey eq '{1}'".format(get_jwt_claims()["id"], id.replace("'", ";"))

        sensordata = table_service.query_entities('sensors', filter=filter)
        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error data not found"}, 400
        connectionstring = sensordata["ConnectionString"]

        filter = "PartitionKey eq {0}".format(connectionstring)
        points = table_service.query_entities('sensordata', filter=filter)
        for point in points:
            point["Timestamp"] = point["Timestamp"].isoformat()

        return {"message": "success", "sensordata": sensordata, "uri": request.base_url}, 200
