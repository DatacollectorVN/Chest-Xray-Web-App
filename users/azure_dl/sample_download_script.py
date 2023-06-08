import os
# from .config.config_reader import ConfigReader
# from .connectors.azure_dl import initialize_storage_account

from azure_dl.config.config_reader import ConfigReader
from azure_dl.connectors.azure_dl import initialize_storage_account


config_reader = ConfigReader(file_name = '/mnt/d/Chest-Xray-Web-App/users/azure_dl/config/config.ini') # '/home/nathan/project/ChestXray-Model-API/app/config/config.ini'
service_client = initialize_storage_account(config_reader.azure_storage['azure_storage_account_name']
    ,  config_reader.azure_storage['azure_storage_account_key']
)
# print(service_client.list_file_systems())
# for i in service_client.list_file_systems():
#     print(i)
file_system_client = service_client.get_file_system_client(file_system='prediction')
file_client = file_system_client.get_file_client(file_path = 'chest_xray/user_id_1/test1.jpeg')

# output_path = os.path.join("/home/nathan/project/ChestXray-Model-API/app/", "images_1.jpeg")
output_path = "/home/Chest-Xray-Web-App/test2.jpeg" # "/mnt/d/Chest-Xray-Web-App/users/azure_dl/test2.jpeg" #/home/Chest-Xray-Web-App
with open(output_path,'wb') as local_file:
    download= file_client.download_file()
    downloaded_bytes = download.readall()
    local_file.write(downloaded_bytes)