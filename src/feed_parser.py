import xml.etree.ElementTree as et
import requests
from src.parsed_item import ParsedItem
from src.str_ext import StrExt
from enum import Enum

class FeedParser:

# Varibles

    all_items = set()
    available_items = set()
    absence_items = set()
    map_ids = dict()


# Instance initialization

    def __init__(self, settings):
        self.settings = settings
        self._parse(settings)
        

# Private methods

    def _parse(self, settings):
        print("Start parsing feed...")
        content = requests.get(settings.feed.url).content
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

            feed = settings.feed
            brand = FeedKey.BRAND.parse(item)
            if brand == feed.brand.lower():                
                category = FeedKey.PRODUCT_TYPE.parse(item)
                if category.startswith(feed.product_type.lower()):                
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
                        self.available_items.add(parsed)
                    else:
                        self.absence_items.add(parsed)
        self.all_items = self.available_items | self.absence_items
        print(f"Found {len(self.all_items)} for category {feed.product_type} for {feed.brand}")
