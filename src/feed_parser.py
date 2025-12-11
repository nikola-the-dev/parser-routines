import xml.etree.ElementTree as et
import requests
from src.parsed_item import ParsedItem
from src.str_ext import StrExt

class FeedParser:

# Varibles

    items = dict()


# Instance initialization

    def __init__(self, settings):
        self.settings = settings
        self._parse(settings)
        

# Private methods

    def _parse(self, settings):
        content = requests.get(settings.feed.url).content
        root = et.fromstring(content)
        items = root.find("channel").findall("item")
        ns = {"g": "http://base.google.com/ns/1.0"}
        for item in items:            
            category = item.find("g:product_type", ns).text.lower()
            if category.startswith(settings.feed.product_type.lower()):
                brand = item.find("g:brand", ns).text.lower()                 
                if brand == settings.feed.brand.lower():                
                    sku = item.find("g:mpn", ns).text.lower()                                     

                    parsed = ParsedItem()                    
                    parsed.sku = sku
                    parsed.href = item.find("g:link", ns).text
                    parsed.old_price = StrExt.digits(item.find("g:price", ns).text)                                     
                    parsed.new_price = StrExt.digits(item.find("g:sale_price", ns).text)                                     
                    availability = item.find("g:availability", ns).text.lower()
                    match availability:
                        case "in stock":
                            parsed.stock = ParsedItem.Stock.IN_STOCK
                        case "preorder":
                            parsed.stock = ParsedItem.Stock.WAITING
                        case _:
                            parsed.stock = ParsedItem.Stock.OUT_STOCK

                    self.items[sku] = parsed

                    # g:availability - in stock - preorder - out of stock
                    # preorder - Очікується
                    # g:mpn
                    # g:sale_price
                    # g:price
