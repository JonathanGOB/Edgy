from pymongo import MongoClient
from collections import OrderedDict

client = MongoClient('13.95.226.151', 27017)
database = client['iotplatform']

database.create_collection("user")

user_validation = {
    "$jsonschema":{
        "required": ["name", "email", "password", "made at"],
        "properties":{
            "name":{
                "bsonType": "string",
                "description": "must be a string and is required"
            },

            "email":{
                "bsonType": "string",
                "description": "must be a string and is required"
            },

            "password": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },

            "made at": {
                "bsonType": "date",
                "description": "must be a date and is required"
            },
        }
    }
}

query = [('collMod', 'iotplatform'),
        ('validator', user_validation),
        ('validationLevel', 'moderate')]

query = OrderedDict(query)
database.command(query)