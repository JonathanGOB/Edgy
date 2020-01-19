from TableStorage.TableStorageConnection import AzureTableStorage
from azure.cosmosdb.table.tablebatch import TableBatch

class Cascade():

    def __init__(self, jwt_claims, rowkey, *args):
        self.jwt_claims = jwt_claims
        self.entities = args[0][0]
        self.key = rowkey
        self.tables = args[0][1]
        self.table_service = AzureTableStorage().get_table()

    def delete(self):
        start = False
        keys = []

        return_entity = None
        for i in range(len(self.entities)):
            print(keys)
            if start:
                if self.entities[i] != "ConnectionString":
                    localKeys = []
                    for key in keys:
                        filter = "OwnerId eq '{0}' and {1} eq '{2}'".format(self.jwt_claims["id"], self.entities[i], key)
                        rows = self.table_service.query_entities(self.tables[i], filter=filter)
                        if len(list(rows)) > 0:
                            rows = list(rows)
                        else:
                            return return_entity
                        for row in rows:
                            localKeys.append(row["RowKey"])
                            self.table_service.delete_entity(self.tables[i], row["PartitionKey"], row["RowKey"])
                    keys = localKeys

                if self.entities[i] == "ConnectionString":
                    for key in keys:
                        filter = "OwnerId eq '{0}' and {1} eq '{2}'".format(self.jwt_claims["id"], "PartitionKey", key)
                        rows = self.table_service.query_entities(self.tables[i], filter=filter)
                        if len(list(rows)) > 0:
                            rows = list(rows)
                        else:
                            return return_entity
                        for row in rows:
                            self.table_service.delete_entity(self.tables[i], row["PartitionKey"], row["RowKey"])

            if not start:
                filter = "OwnerId eq '{0}' and RowKey eq '{1}'".format(self.jwt_claims["id"], self.key)
                row = self.table_service.query_entities(self.tables[i], filter=filter)
                if len(list(row)) > 0:
                    row = list(row)[0]
                else:
                    return return_entity
                keys.append(self.key)
                return_entity = row
                self.table_service.delete_entity(self.tables[i], row["PartitionKey"], row["RowKey"])

                start = True
        return return_entity

