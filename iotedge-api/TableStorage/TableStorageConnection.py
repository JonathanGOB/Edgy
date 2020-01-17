from azure.cosmosdb.table.tableservice import TableService
from Settings import ConfigTableStorage


class AzureTableStorage():
    table_service = None

    def __init__(self):
        # get connection with the table storage
        self.table_service = TableService(account_name=ConfigTableStorage.username,
                                          account_key=ConfigTableStorage.account_key)

    def get_table(self):
        return self.table_service
