import configparser
import sys
import os


class Settings:

# Constants

    class Key:
        source = "Source"
        feed = "Feed"
        output = "Output"
        url = "url"
        category_path = "category_path"
        page_argumnet = "page_argumnet"
        product_type = "product_type"
        product_brand = "product_brand"
        column_names = "column_names"
        stock_names = "stock_names"


    class BaseItem:
        url = ""

        def __init__(self, section):
            self.url = section[Settings.Key.url]


    class Soucre(BaseItem):
        category_path = ""
        page_argument = ""

        def __init__(self, section):
            super().__init__(section)
            keys = Settings.Key
            self.category_path = section[keys.category_path]
            self.page_argument = section[keys.page_argumnet]


    class Feed(BaseItem):
        product_type = ""
        brand = ""

        def __init__(self, section):
            super().__init__(section)
            keys = Settings.Key
            self.product_type = section[keys.product_type]
            self.brand = section[keys.product_brand]


    class Output:
        sku_col_name = ""
        stock_col_name = ""
        stock_names = []

        def __init__(self, section):
            keys = Settings.Key
            cols = section[keys.column_names]
            self.sku_col_name, self.stock_col_name = [item.strip() for item in cols.split(",")]
            self.stock_names = [item.strip() for item in section[keys.stock_names].split(",")]


# Variables


# Instance initialization

    def __init__(self, config_path):
        if os.path.exists(config_path):
            self.read_configs(config_path)
        else:
            print("Config file doesn't exists")
            sys.exit()


# Private methods
    
    def read_configs(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        self.feed = Settings.Feed(config[self.Key.feed])
        self.source = Settings.Soucre(config[self.Key.source])       
        self.output = Settings.Output(config[self.Key.output]) 
