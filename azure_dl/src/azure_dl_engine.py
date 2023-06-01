import os, uuid, sys

def upload_file(service_client, src_path, file_system_name, directory_path, output_file):
    try:
        state = True
        file_system_client = service_client.get_file_system_client(file_system = file_system_name)
        directory_client = file_system_client.get_directory_client(directory = directory_path)
        with open(src_path, "rb") as file:
            file_system_client = directory_client.create_file(output_file)
            file_system_client.upload_data(file,  overwrite=True)
    except Exception as e:
        state = False
    return state

def dowload_file(service_client, file_system_name, file_path, output_path):
    try:
        state = True
        file_system_client = service_client.get_file_system_client(file_system = file_system_name)
        file_client = file_system_client.get_file_client(file_path = file_path)

        with open(output_path,'wb') as local_file:
            download= file_client.download_file()
            downloaded_bytes = download.readall()
            local_file.write(downloaded_bytes)
            
    except Exception as e:
        state = False
    return state
