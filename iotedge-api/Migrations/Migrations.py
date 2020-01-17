from azure.cosmosdb.table.models import Entity
from TableStorage.TableStorageConnection import AzureTableStorage

storageclass = AzureTableStorage()
table_service = storageclass.get_table()

def maketable(table_service, name):
    print("creating table with table name: {0}".format(name))
    table_service.create_table(name)

def insertentity(table_service, entity, table):
    print("inserting row with PartitionKey: {0}".format(entity.PartitionKey))
    table_service.insert_entity(table, entity)

#create tables in table storage
try:
    maketable(table_service, 'users')
    maketable(table_service, 'edgedevices')
    maketable(table_service, 'sensors')
    maketable(table_service, 'sensorsdevices')
    maketable(table_service, 'sensordata')
    maketable(table_service, 'rulers')
    maketable(table_service, 'revokedtokens')

except Exception as e:
    raise Exception("cannot make tables: ", e)



# create rulers for all schemas
user_table = Entity()
user_table.PartitionKey = 'users'
user_table.RowKey = '0'
user_table.NewId = 0
user_table.Size = 0

edgedevices_table = Entity()
edgedevices_table.PartitionKey = 'edgedevices'
edgedevices_table.RowKey = '1'
edgedevices_table.NewId = 0
edgedevices_table.Size = 0

sensors_table = Entity()
sensors_table.PartitionKey = 'sensors'
sensors_table.RowKey = '2'
sensors_table.NewId = 0
sensors_table.Size = 0

sensordevices_table = Entity()
sensordevices_table.PartitionKey = 'sensordevices'
sensordevices_table.RowKey = '3'
sensordevices_table.NewId = 0
sensordevices_table.Size = 0

sensordata_table = Entity()
sensordata_table.PartitionKey = 'sensordata'
sensordata_table.RowKey = '4'
sensordata_table.NewId = 0
sensordata_table.Size = 0

rulers_table = Entity()
rulers_table.PartitionKey = 'rulers'
rulers_table.RowKey = '5'
rulers_table.NewId = 7
rulers_table.Size = 7

revokedtokens_table = Entity()
revokedtokens_table.PartitionKey = 'revokedtokens'
revokedtokens_table.RowKey = '6'
revokedtokens_table.NewId = 0
revokedtokens_table.Size = 0

# batch insertion
insertentity(table_service, user_table, 'rulers')
insertentity(table_service, edgedevices_table, 'rulers')
insertentity(table_service, sensors_table, 'rulers')
insertentity(table_service, sensordevices_table, 'rulers')
insertentity(table_service, sensordata_table, 'rulers')
insertentity(table_service, rulers_table, 'rulers')
insertentity(table_service, revokedtokens_table, 'rulers')

print("successful migration")