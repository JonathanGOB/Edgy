from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

#get connection with the table storage
try:
    table_service = TableService(account_name='stagerobbeoesmandiag', account_key='oZdA2sPZtAM1ZtLOEN/MHKluqOHmDahNagJqR/VasbFVRSYvxj947Zz4Tf0mjA5EwYME0/Bj5l2JF/ZQEOjHSQ==')
except Exception as e:
    raise Exception("cannot create connection: ", e)


#create tables in table storage
try:
    table_service.create_table('users')
    table_service.create_table('edgedevices')
    table_service.create_table('sensors')
    table_service.create_table('sensorsdevice')
    table_service.create_table('sensordata')

except Exception as e:
    raise Exception("cannot make tables: ", e)

print("successful migration")