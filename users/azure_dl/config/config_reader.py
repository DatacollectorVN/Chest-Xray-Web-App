import configparser
import os
import ast


class ConfigReader(object):
    def __init__(self, file_name):
        config = configparser.ConfigParser()
        config_conf_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), file_name
            )
        )
        found = config.read(config_conf_path)
        if not found:
            raise ValueError('No config file found!')

        for section in config.sections():
            self.__dict__.__setitem__(section, {}) # add attrribute
            for sub_section in config.options(section):
                item = config.get(section, sub_section)
                if item.startswith('{') and item.endswith('}'):
                    item = ast.literal_eval(item) # https://docs.python.org/3/library/ast.html#ast.literal_eval
                
                if item.startswith('"') and item.endswith('"'):
                    item = item.strip('"')
                
                self.__getattribute__(section)[sub_section] = item # add value into attribute


config_reader = ConfigReader(file_name = 'config.ini')

if __name__ == '__main__':
    print(config_reader.azure_storage['azure_storage_connection_string'])
    print()