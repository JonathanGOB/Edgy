from azure.cosmosdb.table.tableservice import TableService
from TableStorageConnection import AzureTableStorage

storageclass = AzureTableStorage()
table_service = storageclass.get_table()

#create tables in table storage
try:
    table_service.create_table('users')
    table_service.create_table('edgedevices')
    table_service.create_table('sensors')
    table_service.create_table('sensorsdevices')
    table_service.create_table('sensordata')

except Exception as e:
    raise Exception("cannot make tables: ", e)

print("successful migration")