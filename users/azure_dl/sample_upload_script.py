import os
from config.config_reader import ConfigReader
from connectors.azure_dl import initialize_storage_account

# from azure_dl.config.config_reader import ConfigReader
# from azure_dl.connectors.azure_dl import initialize_storage_account


config_reader = ConfigReader(file_name = '/mnt/d/Chest-Xray-Web-App/users/azure_dl/config/config.ini') # '/home/nathan/project/ChestXray-Model-API/app/config/config.ini'
service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
    ,  config_reader.azure_storage['azure_storage_account_key']
)
# print(service_client.list_file_systems())
# for i in service_client.list_file_systems():
#     print(i)
file_system_client = service_client.get_file_system_client(file_system='prediction')   
directory_client = service_client.get_directory_client(file_system_client.file_system_name, 'output_images') # "chest_xray"
with open("/mnt/d/Chest-Xray-Web-App/users/azure_dl/output_image_9_1.jpg", "rb") as file:
    file_system_client = directory_client.create_file("output_image_9_1.jpg") # output_image_9_1.jpg
    file_system_client.upload_data(file,  overwrite=True)

    
    
# file_client.upload_file(service_client, src_path, file_system_name, directory_path, output_file)