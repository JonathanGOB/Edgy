from TableStorage.TableStorageConnection import AzureTableStorage
import threading

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
            isNew = True
        except:
            print("concurrency problems")


        try:
            sensors_fields = {
                "PartitionKey": sensordata["PartitionKey"].replace("'", ";"),
                "RowKey": str(sensordata_table["NewId"]),
                "Datavalue": sensordata["Datavalue"]
            }

            table_service.insert_entity('sensordata', sensors_fields)
        except Exception as e:
            print("error: ", e)


if __name__ == '__main__':
    thread1 = threading.Thread(target=loop)
    thread1.start()