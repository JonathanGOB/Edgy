import time
import datetime
import os
import sys
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message
import uuid
import json
import random

# GLOBALS
MESSAGECOUNTER = 0
TWIN_CALLBACKS = 0

PUSHSENSORDEVICECORRELATION = "9854"
PUSHSENSORCORRELATION = "7355"
PUSHSENSORDATACORRELATION = "4244"
ROWKEYSEPARATOR = ">"

# Message types
PushSensorDevice = {
    "Cmd": "PushSensorDevice",
    "Corr": "9854"
}
PushSensor = {
    "Cmd": "PushSensor",
    "Corr": "7355"
}
PushSensorData = {
    "Cmd": "PushSensorData",
    "Corr": "4244"
}

SensorDevicePropertiesSet = False
SensorDevicePropertiesSent = False
SensorDeviceProperties = {
    "ForeignKeyEdgeDevice": "",
    "UniqueSensorDeviceId": "",
    "RowKey": "",
    "PartitionKey": "",
    "Protocol": "",
    "Location": "",
    "Description": "",
    "Created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
SensorProperties = []
SensorPropertiesSet = []
SensorPropertiesSent = []

def PropertiesComplete(Properties: dict):
    AllPropertiesSet = True
    for item in Properties.keys():
        AllPropertiesSet &= (len(Properties[item]) > 0)
    return AllPropertiesSet

def UpdateProperties(Twin: dict):
    global SensorDevicePropertiesSet, SensorDevicePropertiesSent
    
    Timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Updating properties")
    if "UniqueSensorDeviceId" in Twin:
        SensorDeviceProperties["UniqueSensorDeviceId"] = Twin["UniqueSensorDeviceId"]
        for Sensor in SensorProperties:
            Sensor["ForeignKeySensorDevice"] = Twin["UniqueSensorDeviceId"]
            Sensor["Updated"] = Timestamp
        SensorDeviceProperties["Updated"] = Timestamp
        print("Received module name")

    if "ForeignKeyEdgeDevice" in Twin:
        SensorDeviceProperties["ForeignKeyEdgeDevice"] = Twin["ForeignKeyEdgeDevice"]
        # for Sensor in SensorProperties:
        #     Sensor["ForeignKeySensorDevice"] = Twin["ForeignKeyEdgeDevice"]
        #     Sensor["Updated"] = Timestamp
        SensorDeviceProperties["Updated"] = Timestamp
        print("Received edge device id")
        
    if "Location" in Twin:
        SensorDeviceProperties["Location"] = Twin["Location"]
        for Sensor in SensorProperties:
            Sensor["Location"] = Twin["Location"]
            Sensor["Updated"] = Timestamp
        SensorDeviceProperties["Updated"] = Timestamp
        print("Received SensorDevice location")
    
    if "Protocol" in Twin:
        SensorDeviceProperties["Protocol"] = Twin["Protocol"]
        SensorDeviceProperties["Updated"] = Timestamp
        print("Received SensorDevice location")

    if "Description" in Twin:
        SensorDeviceProperties["Description"] = Twin["Description"]
        SensorDeviceProperties["Updated"] = Timestamp
        print("Received SensorDevice description")

    if "PartitionKey" in Twin:
        SensorDeviceProperties["PartitionKey"] = Twin["PartitionKey"]
        # for Sensor in SensorProperties:
        #     Sensor["PartitionKey"] = Twin["PartitionKey"]
        #     Sensor["Updated"] = Timestamp
        SensorDeviceProperties["RowKey"] = ROWKEYSEPARATOR
        SensorDeviceProperties["Updated"] = Timestamp

    SensorDevicePropertiesSet = PropertiesComplete(SensorDeviceProperties)
    
    if "Sensors" in Twin:
        for Key, Value in Twin["Sensors"].items():
            # Check if sensor object already exists
            Sensorindex = None
            for index in range(0, len(SensorProperties)):
                if(SensorProperties[index]["UniqueSensorId"] == Key):
                    Sensorindex = index
                    break

            if(Sensorindex == None):
                # Add new sensor to the list
                SensorPropertiesTemplate = {
                    "ForeignKeySensorDevice": "",
                    "UniqueSensorId": "",
                    "PartitionKey": "",
                    "RowKey": "",
                    "Name": "",
                    "Datatype": "",
                    "Location": "",
                    "Description": "",
                    "Created": Timestamp,
                    "Updated": Timestamp
                }
                
                SensorPropertiesTemplate["UniqueSensorId"] = Key
                SensorPropertiesTemplate["Updated"] = Timestamp

                if "Name" in Value:
                    SensorPropertiesTemplate["Name"] = Value["Name"]
                    SensorPropertiesTemplate["Updated"] = Timestamp

                if "Datatype" in Value:
                    SensorPropertiesTemplate["Datatype"] = Value["Datatype"]
                    SensorPropertiesTemplate["Updated"] = Timestamp

                if "Description" in Value:
                    SensorPropertiesTemplate["Description"] = Value["Description"]
                    SensorPropertiesTemplate["Updated"] = Timestamp
                
                if "PartitionKey" in Value:
                    SensorPropertiesTemplate["PartitionKey"] = Value["PartitionKey"]
                    SensorPropertiesTemplate["Updated"] = Timestamp
                
                if(SensorDevicePropertiesSet):
                    SensorPropertiesTemplate["ForeignKeySensorDevice"] = SensorDeviceProperties["UniqueSensorDeviceId"]
                    SensorPropertiesTemplate["Location"] = SensorDeviceProperties["Location"]
                    SensorPropertiesTemplate["RowKey"] = SensorDeviceProperties["RowKey"] + SensorPropertiesTemplate["UniqueSensorId"]
                    SensorPropertiesTemplate["Updated"] = Timestamp
                
                SensorProperties.append(SensorPropertiesTemplate)
                SensorPropertiesSet.append(PropertiesComplete(SensorPropertiesTemplate))
                SensorPropertiesSent.append(False)

            else:
                StoredSensor = SensorProperties[Sensorindex]
                StoredSensor["UniqueSensorId"] = Key
                StoredSensor["Updated"] = Timestamp

                if "Name" in Value:
                    StoredSensor["Name"] = Value["Name"]
                    StoredSensor["Updated"] = Timestamp

                if "Datatype" in Value:
                    StoredSensor["Datatype"] = Value["Datatype"]
                    StoredSensor["Updated"] = Timestamp

                if "Description" in Value:
                    StoredSensor["Description"] = Value["Description"]
                    StoredSensor["Updated"] = Timestamp
                
                if "PartitionKey" in Value:
                    StoredSensor["PartitionKey"] = Value["PartitionKey"]
                    StoredSensor["Updated"] = Timestamp
                
                if(SensorDevicePropertiesSet and not SensorPropertiesSet[Sensorindex]):
                    StoredSensor["ForeignKeySensorDevice"] = SensorDeviceProperties["UniqueSensorDeviceId"]
                    StoredSensor["Location"] = SensorDeviceProperties["Location"]
                    StoredSensor["RowKey"] = SensorDeviceProperties["RowKey"] + StoredSensor["UniqueSensorId"]
                    StoredSensor["Updated"] = Timestamp
                    
                SensorPropertiesSet[Sensorindex] = PropertiesComplete(StoredSensor)
                SensorPropertiesSent[Sensorindex] = False
    print("Printing SensorDevice properties:")
    print(SensorDeviceProperties, "\n\n")
    print("Printing Sensor properties:")
    print(SensorProperties, "\n")

async def SendMessage(client: IoTHubModuleClient, data: dict, command: dict):
    Cmd = {
        "Command":command["Cmd"]
    }
    Cmd.update(data)
    msg = json.dumps(Cmd)
    msg = Message(msg)
    msg.message_id = uuid.uuid4()
    msg.correlation_id = "correlation-" + command["Corr"]
    print("Sending message:")
    print(msg)
    try:
        await client.send_message_to_output(msg, "UpstreamOutput")
    except Exception as ex:
        print ( "Unexpected error in sender: %s" % ex )
    print("Finished sending")

# Random Data generator
async def DataGenerator(client: IoTHubModuleClient):
    try:
        while(True):
            print("Sending updates")
            for Sensor in range(0, len(SensorProperties)):
                if(SensorPropertiesSet[Sensor]):
                    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    SensorData = {
                        "ForeignKeySensorDevice": SensorProperties[Sensor]["ForeignKeySensorDevice"],
                        "ForeignKeySensor": SensorProperties[Sensor]["UniqueSensorId"],
                        # SensorData Row key in the following format:
                        # UniqueSensorDeviceId>UniqueSensorId>Updated
                        "RowKey": SensorProperties[Sensor]["RowKey"] + ROWKEYSEPARATOR + ts,
                        "PartitionKey": SensorProperties[Sensor]["PartitionKey"],
                        "Datavalue": int(random.randint(0, 40)),
                        "Updated": ts
                    }
                    
                    await SendMessage(client, SensorData, PushSensorData)
                else:
                    print("Nothing happened.")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("Exiting data generator")

# publish container details to Azure at startup
async def Setup(client: IoTHubModuleClient):
    global SensorDevicePropertiesSet, SensorDevicePropertiesSent
    try:
        while(True):
            if(SensorDevicePropertiesSet and not SensorDevicePropertiesSent):
                # await SendMessage(client, SensorDeviceProperties, PushSensorDevice)
                SensorDevicePropertiesSent = True
            
            for index in range(0, len(SensorProperties)):
                if(SensorPropertiesSet[index] and not SensorPropertiesSent[index]):
                    await SendMessage(client, SensorProperties[index], PushSensor)
                SensorPropertiesSent[index] = True
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        print("Setup task cancelled")
        
# twin_patch_listener is invoked when the module twin's desired properties are updated.
async def ReceiveTwinProperties(client: IoTHubModuleClient):
    try:
        # Get desired properties
        properties = await client.get_twin()
        print("Received twin properties")
        UpdateProperties(properties["desired"])
        
        # Listen for updates
        while True:
            try:
                data = await client.receive_twin_desired_properties_patch()  # blocking call
                print("Received twin update")
                UpdateProperties(data)
                await asyncio.sleep(10)
            except Exception as ex:
                print ( "Unexpected error in twin_patch_listener: %s" % ex )
    except asyncio.CancelledError:
        print("Receive twin properties task cancelled")

def main():
    try:
        print("Starting now")
        client = IoTHubModuleClient.create_from_edge_environment()
        print("Created client")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.connect())
        print("Connected")
        ReceiveTwinPropertiesTask = loop.create_task(ReceiveTwinProperties(client))
        # SetupTask = loop.create_task(Setup(client))
        DataGeneratorTask = loop.create_task(DataGenerator(client))
        
        while(True):
            loop.run_until_complete(asyncio.sleep(100))
    except KeyboardInterrupt:
        DataGeneratorTask.cancel()
        ReceiveTwinPropertiesTask.cancel()
        # SetupTask.cancel()

if __name__ == "__main__":
    main()