import configparser
import os
from logger import Logger



if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/configparser.ini" 

    if os.path.isfile(filepath):
        parser = configparser.SafeConfigParser()
        parser.read(filepath)
        print(parser.sections())
    else:
        Logger.print_err("No config parser in this folder.")


