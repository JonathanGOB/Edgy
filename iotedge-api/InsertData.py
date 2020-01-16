from TableStorageConnection import AzureTableStorage

table_service = AzureTableStorage().get_table()

# Insert a new entity
task = {'PartitionKey': 'Groningen', 'RowKey': '004',
        'description': 'Buy detergent'}

# Insert a new entity
task1 = {'PartitionKey': 'Groningen', 'RowKey': '005',
        'description': 'Buy detergent'}

# Insert a new entity
task2 = {'PartitionKey': 'Groningen', 'RowKey': '006',
        'description': 'Buy detergent'}

with table_service.batch('users') as batch:
    batch.insert_entity(task)
    batch.insert_entity(task1)
    batch.insert_entity(task2)