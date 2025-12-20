import xml.etree.ElementTree as et
import requests
from src.parsed_item import ParsedItem
from src.str_ext import StrExt
from src.settings import Settings
from enum import Enum


class FeedParser:

# Constants

    class Item:
    
    # Instance initialization

        def __init__(self):
            self.available_items = set()
            self.absence_items = set()

    # Public methods

        def all_items(self):
            return self.available_items | self.absence_items


# Varibles    

    items = dict()
    map_ids = dict()


# Instance initialization

    def __init__(self, settings: Settings):
        self._parse(settings)
        

# Private methods

    def _parse(self, settings: Settings):
        print("Start parsing feed...")
        feed = settings.feed
        content = requests.get(feed.url).content
        root = et.fromstring(content)
        items = root.find("channel").findall("item")
        
        for item in items:            

            class FeedKey(str, Enum):
                PRODUCT_TYPE = "g:product_type"
                BRAND = "g:brand"
                MPN = "g:mpn"
                LINK = "g:link"
                PRICE = "g:price"
                SALE_PRICE = "g:sale_price"
                AVAILABILITY = "g:availability"
                ID = "g:id"

                def parse(self, item, default_value = "", is_lower = True):
                    ns = {"g": "http://base.google.com/ns/1.0"}
                    element = item.find(self.value, ns)
                    if element is not None:
                        result = element.text
                        return result.lower() if is_lower else result
                    return default_value
            
            brand = FeedKey.BRAND.parse(item)
            if brand == feed.brand.lower():                
                product_type = FeedKey.PRODUCT_TYPE.parse(item)
                category = settings.get_category(product_type)
                if category is not None:              
                    feed_item = FeedParser.Item()
                    if category in self.items:
                        feed_item = self.items[category]

                    sku = FeedKey.MPN.parse(item)

                    self.map_ids[sku] = FeedKey.ID.parse(item, sku, False)

                    parsed = ParsedItem()                    
                    parsed.sku = sku
                    parsed.href = FeedKey.LINK.parse(item)
                    parsed.old_price = StrExt.digits(FeedKey.PRICE.parse(item, "0"))                                     
                    parsed.new_price = StrExt.digits(FeedKey.SALE_PRICE.parse(item, "0"))                                     
                    availability = FeedKey.AVAILABILITY.parse(item)
                    parsed.stock = ParsedItem.Stock.get_feed(availability)                    

                    if parsed.stock == ParsedItem.Stock.IN_STOCK:                        
                        feed_item.available_items.add(parsed)
                    else:
                        feed_item.absence_items.add(parsed)
                    self.items[category] = feed_item
        
        for category in self.items:
            feed_item: FeedParser.Item = self.items[category]
            print(f"For {category} found {len(feed_item.available_items)} available items and {len(feed_item.absence_items)} are out of stock items")
