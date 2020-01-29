from TableStorage.TableStorageConnection import AzureTableStorage
import threading
from datetime import datetime
import pytz

table_service = AzureTableStorage().get_table()

def loop():
    sensordataqueue = table_service.query_entities('sensordataqueue')
    for sensordata in sensordataqueue:
        sensordata_table = None

        try:
            filter = "PartitionKey eq 'sensordata'"
            sensordata_table = table_service.query_entities('rulers', filter=filter)
            sensordata_table = list(sensordata_table)[0]
            ruler_sensordata = {"PartitionKey": sensordata_table['PartitionKey'],
                                "RowKey": sensordata_table['RowKey'],
                                "NewId": sensordata_table["NewId"] + 1, "Size": sensordata_table["Size"] + 1}
            table_service.update_entity('rulers', ruler_sensordata, if_match=sensordata_table["etag"])
            try:
                sensors_fields = {
                    "PartitionKey": sensordata["PartitionKey"].replace("'", ";"),
                    "RowKey": str(sensordata_table["NewId"]),
                    "Datavalue": sensordata["Datavalue"],
                    "Made_at": datetime.strptime(sensordata["Updated"], '%Y-%m-%d %H:%M:%S').astimezone(pytz.UTC)
                }

                print(sensors_fields)

                table_service.insert_entity('sensordata', sensors_fields)
                table_service.delete_entity('sensordataqueue', sensordata["PartitionKey"], sensordata["RowKey"])
            except Exception as e:
                print("error: ", e)
        except:
            print("concurrency problems")


if __name__ == '__main__':
    thread1 = threading.Thread(target=loop)
    thread1.start()