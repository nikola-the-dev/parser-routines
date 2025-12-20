import configparser
import sys
import os
from src.str_ext import StrExt


class Settings:

# Constants

    class Key:
        source = "Source"
        feed = "Feed"
        output = "Output"
        url = "url"
        category_pathes = "category_pathes"
        page_argumnet = "page_argumnet"
        product_types = "product_types"
        product_brand = "product_brand"
        column_names = "column_names"
        stock_names = "stock_names"


    class BaseItem:
        url = ""

        def __init__(self, section):
            self.url = section[Settings.Key.url]


    class Soucre(BaseItem):
        category_pathes = list()
        page_argument = ""

        def __init__(self, section):
            super().__init__(section)
            keys = Settings.Key
            self.category_pathes = StrExt.split_to_list(section[keys.category_pathes], True)
            self.page_argument = section[keys.page_argumnet]


    class Feed(BaseItem):
        product_types = list()
        brand = ""

        def __init__(self, section):
            super().__init__(section)
            keys = Settings.Key
            self.product_types = StrExt.split_to_list(section[keys.product_types], True)
            self.brand = section[keys.product_brand]


    class Output:
        sku_col_name = ""
        stock_col_name = ""
        stock_names = []

        def __init__(self, section):
            keys = Settings.Key
            self.sku_col_name, self.stock_col_name = StrExt.split_to_list(section[keys.column_names])
            self.stock_names = StrExt.split_to_list(section[keys.stock_names])


# Variables


# Instance initialization

    def __init__(self, config_path):
        if os.path.exists(config_path):
            self._read_configs(config_path)
        else:
            print("Config file doesn't exists")
            sys.exit()


# Private methods
    
    def _read_configs(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        self.feed = Settings.Feed(config[self.Key.feed])
        self.source = Settings.Soucre(config[self.Key.source])       
        self.output = Settings.Output(config[self.Key.output]) 


# Public methods

    def get_category(self, product_type: str):
        for i, t in enumerate(self.feed.product_types):
            if product_type.startswith(t):
                return self.source.category_pathes[i]
        return None