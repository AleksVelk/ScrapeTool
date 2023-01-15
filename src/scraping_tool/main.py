from neweggclient import NewEggClient

query_params = {
    "pageIndex": 1,
    "pageSize": 60,
    "enableSpaItem": True
}

client = NewEggClient(query_parameters=query_params, no_of_products=100, file_name="test_products")
client.extract_save_products()

