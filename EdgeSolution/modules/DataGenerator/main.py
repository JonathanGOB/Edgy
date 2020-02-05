# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

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

'''
    Data object hierarchy
    --EdgeDevice1
    ----SensorDevice1
    ------Sensor1
    --------SensorData
    ------Sensor2
    --------SensorData
    ------Sensor3
    --------SensorData
    ----SensorDevice2
    ------Sensor1
    --------SensorData
    --EdgeDevice2
    ----SensorDevice1
    ------Sensor1
    --------SensorData
'''

# SensorDevice properties, unique for 1 edge module
SensorDeviceProperties = {
    "ForeignKeyEdgeDevice": "RPI-01",
    "UniqueSensorDeviceId": "",
    # SensorDevice Row key in the following format:
    # ForeignKeyEdgeDevice>UniqueSensorDeviceId
    "RowKey": "",
    "PartitionKey": "",
    "Protocol": "Random data generator",
    "Location": "",
    "Description": "no",
    "Created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Sensor properties, can be multiple per edge module
Sensor1Properties = {
    "ForeignKeySensorDevice": SensorDeviceProperties["UniqueSensorDeviceId"],
    "UniqueSensorId": "Random1",
    "PartitionKey": "",
    # Sensor Row key in the following format:
    # ForeignKeyEdgeDevice>UniqueSensorDeviceId>UniqueSensorId
    "RowKey": "",
    "Name": "Random Data generator 1",
    "Datatype": "Volt",
    "Location": SensorDeviceProperties["Location"],
    "Description": "no",
    "Created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Sensor properties, can be multiple per edge module
Sensor2Properties = {
    "ForeignKeySensorDevice": SensorDeviceProperties["UniqueSensorDeviceId"],
    "UniqueSensorId": "Random2",
    # Sensor Row key in the following format:
    # ForeignKeyEdgeDevice>UniqueSensorDeviceId>UniqueSensorId
    "PartitionKey": "",
    "RowKey": "",
    "Name": "Random Data generator 2",
    "Datatype": "Volt",
    "Location": SensorDeviceProperties["Location"],
    "Description": "no",
    "Created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# SensorData properties, unique per sensor
Sensor1Data = {
    "ForeignKeySensorDevice": Sensor1Properties["ForeignKeySensorDevice"],
    "ForeignKeySensor": Sensor1Properties["UniqueSensorId"],
    # SensorData Row key in the following format:
    # ForeignKeyEdgeDevice>UniqueSensorDeviceId>UniqueSensorId>Updated
    "RowKey": "",
    "PartitionKey": "",
    "Datavalue": 0,
    "Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

Sensor2Data = {
    "ForeignKeySensorDevice": Sensor2Properties["ForeignKeySensorDevice"],
    "ForeignKeySensor": Sensor2Properties["UniqueSensorId"],
    # SensorData Row key in the following format:
    # ForeignKeyEdgeDevice>UniqueSensorDeviceId>UniqueSensorId>Updated
    "RowKey": "",
    "PartitionKey": "",
    "Datavalue": 0,
    "Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Variable to track if all module properties have been initialized. Only then can the module be registered to the database
AllPropertiesSet = False
# Tracks if modules configuration is uploaded to ze database
ModuleSetupCompleted = False
Sensor1SetupCompleted = False
Sensor2SetupCompleted = False

async def main():
    global AllPropertiesSet
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()
        print("Created")
        # connect the client.
        await module_client.connect()
        print(module_client)
        print("Connected")
        data = await module_client.get_twin()
        print("Received twin")
        # print(data)
        data = data["desired"]
        if "UniqueSensorDeviceId" in data:
            SensorDeviceProperties["UniqueSensorDeviceId"] = data["UniqueSensorDeviceId"]
            Sensor1Properties["ForeignKeySensorDevice"] = data["UniqueSensorDeviceId"]
            Sensor2Properties["ForeignKeySensorDevice"] = data["UniqueSensorDeviceId"]
            SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Received module name")

        if "ForeignKeyEdgeDevice" in data:
            SensorDeviceProperties["ForeignKeyEdgeDevice"] = data["ForeignKeyEdgeDevice"]
            SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Received edge device id")
            
        if "Location" in data:
            SensorDeviceProperties["Location"] = data["Location"]
            Sensor1Properties["Location"] = data["Location"]
            Sensor2Properties["Location"] = data["Location"]
            SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Received module location")

        if "Description" in data:
            SensorDeviceProperties["Description"] = data["Description"]
            SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Received module description")

        if "PartitionKey" in data:
            SensorDeviceProperties["PartitionKey"] = data["PartitionKey"]
            SensorDeviceProperties["RowKey"] = ROWKEYSEPARATOR
        
        # Check if all properties are set
        AllPropertiesSet = True
        for item in SensorDeviceProperties.keys():
            AllPropertiesSet &= (len(SensorDeviceProperties[item]) > 0)
        print(AllPropertiesSet)

        # Random Data generator
        async def DataGenerator(module_client):
            global Sensor1SetupCompleted, Sensor2SetupCompleted
            try:
                while(True):
                    if(Sensor1SetupCompleted):
                        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Sensor1Data["RowKey"] = Sensor1Properties["UniqueSensorId"] + ROWKEYSEPARATOR + ts
                        Sensor1Data["PartitionKey"] = Sensor1Properties["PartitionKey"]
                        Sensor1Data["Datavalue"] = int(random.randint(0, 40))
                        Sensor1Data["Updated"] = ts
                        Command1 = {
                            "Command":"PushSensorData"
                        }
                        Command1.update(Sensor1Data)
                        msg = json.dumps(Command1)
                        print(msg, '\n')
                        await module_client.send_message_to_output(msg, "UpstreamOutput")
                    await asyncio.sleep(5)
                    
                    if(Sensor2SetupCompleted):
                        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Sensor2Data["RowKey"] = Sensor2Properties["UniqueSensorId"] + ROWKEYSEPARATOR + ts
                        Sensor2Data["PartitionKey"] = Sensor2Properties["PartitionKey"]
                        Sensor2Data["Datavalue"] = int(random.randint(0, 40))
                        Sensor2Data["Updated"] = ts
                        Command2 = {
                            "Command":"PushSensorData"
                        }
                        Command2.update(Sensor2Data)
                        msg = json.dumps(Command2)
                        print(msg, '\n')
                        await module_client.send_message_to_output(msg, "UpstreamOutput")
                    await asyncio.sleep(5)

            except asyncio.CancelledError:
                print("Exiting data generator")

        # publish container details to Azure at startup
        async def Setup(module_client):
            global ModuleSetupCompleted, Sensor1SetupCompleted, Sensor2SetupCompleted, AllPropertiesSet
            while(True):
                if(ModuleSetupCompleted and not Sensor1SetupCompleted):
                    Sensor1Properties["RowKey"] = SensorDeviceProperties["RowKey"] + Sensor1Properties["UniqueSensorId"]
                    Command = {
                        "Command":"PushSensor"
                    }
                    Command.update(Sensor1Properties)
                    Command = json.dumps(Command)
                    print(Command)
                    msg = Message(Command)
                    msg.message_id = uuid.uuid4()
                    msg.correlation_id = "correlation-" + PUSHSENSORCORRELATION
                    await module_client.send_message_to_output(msg, "UpstreamOutput")
                    Sensor1SetupCompleted = True

                if(ModuleSetupCompleted and not Sensor2SetupCompleted):
                    Sensor2Properties["RowKey"] = SensorDeviceProperties["RowKey"] + Sensor2Properties["UniqueSensorId"]
                    
                    Command = {
                        "Command":"PushSensor"
                    }
                    Command.update(Sensor2Properties)
                    Command = json.dumps(Command)
                    print(Command)
                    msg = Message(Command)
                    msg.message_id = uuid.uuid4()
                    msg.correlation_id = "correlation-" + PUSHSENSORCORRELATION
                    await module_client.send_message_to_output(msg, "UpstreamOutput")
                    Sensor2SetupCompleted = True

                if(AllPropertiesSet and not ModuleSetupCompleted):
                    # Update properties of SensorDevice, Sensor, and SensorData objects
                    Sensor1Properties["ForeignKeySensorDevice"] = SensorDeviceProperties["UniqueSensorDeviceId"]
                    Sensor1Properties["Location"] = SensorDeviceProperties["Location"]
                    Sensor1Properties["PartitionKey"] = SensorDeviceProperties["PartitionKey"]
                    Sensor1Data["PartitionKey"] = Sensor1Properties["PartitionKey"]
                    
                    Sensor2Properties["ForeignKeySensorDevice"] = SensorDeviceProperties["UniqueSensorDeviceId"]
                    Sensor2Properties["Location"] = SensorDeviceProperties["Location"]
                    Sensor2Properties["PartitionKey"] = SensorDeviceProperties["PartitionKey"]
                    Sensor2Data["PartitionKey"] = Sensor2Properties["PartitionKey"]
                    
                    # Properties can be uploaded to ze database
                    Command = {
                        "Command":"PushSensorDevice"
                    }
                    Command.update(SensorDeviceProperties)
                    Command = json.dumps(Command)
                    print(Command)
                    msg = Message(Command)
                    msg.message_id = uuid.uuid4()
                    msg.correlation_id = "correlation-" + PUSHSENSORDEVICECORRELATION
                    await module_client.send_message_to_output(msg, "UpstreamOutput")
                    ModuleSetupCompleted = True
                await asyncio.sleep(2)
        
        # twin_patch_listener is invoked when the module twin's desired properties are updated.
        async def twin_patch_listener(module_client):
            global TWIN_CALLBACKS, AllPropertiesSet, ModuleSetupCompleted
            while True:
                try:
                    data = await module_client.receive_twin_desired_properties_patch()  # blocking call
                    print( "The data in the desired properties patch was: %s" % data)
                    if "UniqueSensorDeviceId" in data:
                        SensorDeviceProperties["UniqueSensorDeviceId"] = data["UniqueSensorDeviceId"]
                        SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("Received module name")

                    if "ForeignKeyEdgeDevice" in data:
                        SensorDeviceProperties["ForeignKeyEdgeDevice"] = data["ForeignKeyEdgeDevice"]
                        SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("Received edge device id")
                        
                    if "Location" in data:
                        SensorDeviceProperties["Location"] = data["Location"]
                        SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("Received module location")

                    if "Description" in data:
                        SensorDeviceProperties["Description"] = data["Description"]
                        SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("Received module description")

                    if "Created" in data:
                        SensorDeviceProperties["Created"] = data["Created"]
                        SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("Received creation timestamp")
                    
                    if "PartitionKey" in data:
                        SensorDeviceProperties["PartitionKey"] = data["PartitionKey"]
                        SensorDeviceProperties["RowKey"] = ROWKEYSEPARATOR
                        SensorDeviceProperties["Updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print("Received Partition Key")
                    # Check if all properties are set
                    AllPropertiesSet = True
                    for item in SensorDeviceProperties.keys():
                        AllPropertiesSet &= (len(SensorDeviceProperties[item]) > 0)
                    ModuleSetupCompleted = False

                    TWIN_CALLBACKS += 1
                    print ( "Total calls confirmed: %d\n" % TWIN_CALLBACKS )
                except Exception as ex:
                    print ( "Unexpected error in twin_patch_listener: %s" % ex )
        
        # define behavior for receiving an input message on input1
        async def input1_listener(module_client):
            while True:
                input_message = await module_client.receive_message_on_input("input1")  # blocking call
                # print("the data in the message received on input1 was ")
                # print(input_message.data)
                # print("custom properties are")
                # print(input_message.custom_properties)

        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    selection = input("Press Q to quit\n")
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(10)

        # Schedule task for C2D Listener
        listeners = asyncio.gather(
            input1_listener(module_client), 
            twin_patch_listener(module_client), 
            Setup(module_client), 
            DataGenerator(module_client)
            )

        print ( "The sample is now waiting for messages. ")

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel listening
        listeners.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())