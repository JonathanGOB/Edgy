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

    # Get all SensorData by owner
    @jwt_required
    def get(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        filter = "OwnerId eq '{0}'".format(get_jwt_claims()["id"])

        connectionstrings = []
        sensors = table_service.query_entities('sensors', filter=filter)
        for sensor in sensors:
            connectionstrings.append(sensor["ConnectionString"])

        sensordatas = []
        for connectionstring in connectionstrings:
            filter = "PartitionKey eq '{0}'".format(connectionstring)
            sensordata = table_service.query_entities('sensordata', filter=filter)
            if len(list(sensordatas)) > 0:
                for point in sensordata:
                    sensordatas.append(point)

        for row in sensordatas:
            row["Timestamp"] = row["Timestamp"].isoformat()
        return {"message": "success", "data": {"sensordata": sensordatas, "uri": request.base_url}}, 200

    # Post new SensorData

    @jwt_required
    def post(self):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        isNew = False
        while not isNew:
            try:
                filter = "PartitionKey eq 'sensordata'"
                sensordata_table = table_service.query_entities('rulers', filter=filter)
                sensordata_table = list(sensordata_table)[0]
                ruler_sensordata = {"PartitionKey": sensordata_table['PartitionKey'],
                                    "RowKey": sensordata_table['RowKey'],
                                    "NewId": sensordata_table["NewId"] + 1, "Size": sensordata_table["Size"] + 1}
                table_service.update_entity('rulers', ruler_sensordata, if_match=sensordata_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        filter = "ConnectionString eq '{0}'".format(args["ConnectionString"])
        sensor = list(table_service.query_entities('sensors', filter=filter))[0]

        if (len(sensor) > 0):
            if sensor["OwnerId"] == get_jwt_claims()["id"]:
                try:
                    sensors_fields = {
                        "PartitionKey": args["ConnectionString"].replace("'", ";"),
                        "RowKey": str(sensordata_table["NewId"]),
                        "Datavalue": args["Datavalue"].replace("'", ";"),
                    }
                except:
                    return {"message": "fill all data"}, 400

                table_service.insert_entity('sensordata', sensors_fields)

                return {"message": "success", "data": {"sensordata": sensors_fields}}, 200
            else:
                return {"message": "not your sensor"}, 400
        else:
            return {"message": "sensor not found"}, 400


class SingleSensorData(Resource):

    # Get SensorData by id and partitionkey
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
            return {"message": "error id not found"}, 400

        filter = "RowKey eq '{0}'".format(specification)
        sensordata = table_service.query_entities('sensordata', filter=filter)

        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error data not found"}, 400

        connectionstring = sensordata["ConnectionString"]
        filter = "ConnectionString eq '{0}' and OwnerId eq '{1}'".format(connectionstring, get_jwt_claims()["id"])

        sensor = table_service.query_entities('sensors', filter=filter)

        if len(list(sensor)) > 0:
            sensordata["Timestamp"] = sensordata["Timestamp"].isoformat()
            return {"message": "success", "data": {"sensordata": sensordata, "uri": request.base_url}}, 200
        else:
            return {"message": "not your sensordata"}

    # Update SensorData by id
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

        filter = "RowKey eq '{0}'".format(specification)
        sensordata = table_service.query_entities('sensordata', filter=filter)

        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error data not found"}, 400

        connectionstring = sensordata["ConnectionString"]
        filter = "ConnectionString eq '{0}' and OwnerId eq '{1}'".format(connectionstring, get_jwt_claims()["id"])

        sensor = table_service.query_entities('sensors', filter=filter)

        if len(list(sensor)) > 0:
            try:
                sensordata["PartitionKey"] = args["ConnectionString"].replace("'", ";")
                sensordata["Name"] = args["Name"].replace("'", ";")
                sensordata["Datavalue"] = args["Datavalue"].replace("'", ";")
                del sensordata["etag"]
            except:
                return {"message": "fill data"}, 400

            table_service.update_entity('sensordata', sensordata)

            sensordata["Timestamp"] = sensordata["Timestamp"].isoformat()
            return {"message": "success", "data": {"sensordata": sensordata, "uri": request.base_url}}, 200
        else:
            return {"message": "not your sensordata"}

    # Delete SensorData by id
    @jwt_required
    def delete(self, id):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()
        args = parser.parse_args()

        isNew = False
        while not isNew:
            try:
                filter = "PartitionKey eq 'sensordata'"
                sensordata_table = table_service.query_entities('rulers', filter=filter)
                sensordata_table = list(sensordata_table)[0]
                ruler_sensordata = {"PartitionKey": sensordata_table['PartitionKey'],
                                    "RowKey": sensordata_table['RowKey'],
                                    "NewId": sensordata_table["NewId"], "Size": sensordata_table["Size"] - 1}
                table_service.update_entity('rulers', ruler_sensordata, if_match=sensordata_table["etag"])
                isNew = True
            except:
                print("concurrency problems")

        specification = None
        searcher = None

        if id:
            specification = id.replace("'", ";")
            searcher = "RowKey"

        else:
            return {"message": "error device not found"}, 400

        filter = "RowKey eq '{0}'".format(specification)
        sensordata = table_service.query_entities('sensordata', filter=filter)

        if len(list(sensordata)) > 0:
            sensordata = list(sensordata)[0]
        else:
            return {"message": "error data not found"}, 400

        connectionstring = sensordata["ConnectionString"]
        filter = "ConnectionString eq '{0}' and OwnerId eq '{1}'".format(connectionstring, get_jwt_claims()["id"])

        sensor = table_service.query_entities('sensors', filter=filter)

        if len(list(sensor)) > 0:
            table_service.delete_entity('sensordata', sensordata["PartitionKey"], sensordata["RowKey"])

            return {"message": "success deleted sensordata {}".format(sensordata["Name"])}, 200
        else:
            return {"message": "not your sensordata"}


class GetSensorSensorData(Resource):

    # Get all SensorData from ConnectionString
    @jwt_required
    def get(self, id, partitionkey):
        storage = AzureTableStorage()
        table_service = storage.get_table()
        verify_jwt_in_request()

        filter = "OwnerId eq '{0}' and RowKey eq '{1}' and PartitionKey '{2}'".format(get_jwt_claims()["id"],
                                                                                      id.replace("'", ";"),
                                                                                      partitionkey.replace("'", ";"))

        sensor = table_service.query_entities('sensors', filter=filter)
        if len(list(sensor)) > 0:
            sensor = list(sensor)[0]
        else:
            return {"message": "error data not found"}, 400
        connectionstring = sensor["ConnectionString"]
        filter = "PartitionKey eq '{0}'".format(connectionstring)
        points = table_service.query_entities('sensordata', filter=filter)

        if len(list(points)) > 0:
            sensordata = list(points)
        else:
            return {"message": "error data not found"}, 400

        for point in sensordata:
            point["Timestamp"] = point["Timestamp"].isoformat()

        return {"message": "success", "data": {"sensordata": sensordata, "uri": request.base_url}}, 200
