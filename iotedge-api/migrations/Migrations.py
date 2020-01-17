from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from TableStorageConnection import AzureTableStorage
from azure.cosmosdb.table.tablebatch import TableBatch

storageclass = AzureTableStorage()
table_service = storageclass.get_table()

#create tables in table storage
try:
    table_service.create_table('users')
    table_service.create_table('edgedevices')
    table_service.create_table('sensors')
    table_service.create_table('sensorsdevices')
    table_service.create_table('sensordata')
    table_service.create_table('rulers')
    table_service.create_table('revokedtokens')

except Exception as e:
    raise Exception("cannot make tables: ", e)

# create rulers for all schemas
user_table = Entity()
user_table.PartitionKey = 'ruler'
user_table.RowKey = 0
user_table.LastId = 0
user_table.Size = 0

edgedevices_table = Entity()
edgedevices_table.PartitionKey = 'ruler'
edgedevices_table.RowKey = 1
edgedevices_table.LastId = 0
edgedevices_table.Size = 0

sensors_table = Entity()
sensors_table.PartitionKey = 'ruler'
sensors_table.RowKey = 2
sensors_table.LastId = 0
sensors_table.Size = 0

sensordevices_table = Entity()
sensordevices_table.PartitionKey = 'ruler'
sensordevices_table.RowKey = 3
sensordevices_table.LastId = 0
sensordevices_table.Size = 0

sensordata_table = Entity()
sensordata_table.PartitionKey = 'ruler'
sensordata_table.RowKey = 4
sensordata_table.LastId = 0
sensordata_table.Size = 0

rulers_table = Entity()
rulers_table.PartitionKey = 'ruler'
rulers_table.RowKey = 5
rulers_table.LastId = 6
rulers_table.Size = 7

revokedtokens_table = Entity()
revokedtokens_table.PartitionKey = 'ruler'
revokedtokens_table.RowKey = 6
revokedtokens_table.LastId = 0
revokedtokens_table.Size = 0

# batch insertion
batch = TableBatch()
batch.insert_entity(user_table)
batch.insert_entity(edgedevices_table)
batch.insert_entity(sensors_table)
batch.insert_entity(sensordevices_table)
batch.insert_entity(sensordata_table)
batch.insert_entity(rulers_table)
batch.insert_entity(revokedtokens_table)

table_service.commit_batch('users', batch)
print("successful migration")