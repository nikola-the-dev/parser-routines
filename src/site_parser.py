from bs4 import BeautifulSoup
import requests
from urllib.parse import urlunsplit, urlencode
import re
from src.parsed_item import ParsedItem
from src.str_ext import StrExt


class SiteParser:

# Variables

    currentPage = 1
    items = dict()
    reaches_end = False


# Instance initialization

    def __init__(self, settings):
        self.settings = settings
        self.parse()


# Private methods        

    def _get_page_url(self):
        source = self.settings.source
        query_params = {source.page_argument: self.currentPage}
        query_string = urlencode(query_params)
        pattern = r"https?://(www\.)?"
        domain = re.sub(pattern, "", source.url)
        return urlunsplit(("https", domain, source.category_path, query_string, ""))


    def _get_next_page(self):        
        if self.reaches_end:
            return        
        
        def price_pair(source):
            p_old = "0"
            p_new = "0"
            price_comp = source.find("span", class_="price-new")
            old_price_comp = source.find("span", class_="price-old")
            if (price_comp is not None) and (old_price_comp is not None):
                p_old = StrExt.digits(old_price_comp.get_text())
                p_new = StrExt.digits(price_comp.get_text())    
            else:        
                price_comp = source.find("p", class_="price")
                if price_comp is not None:
                    p_old = StrExt.digits(price_comp.get_text())            
            return (int(p_old), int(p_new))
        
        url = self._get_page_url()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_="product-qty")
        for item in items:
            parent = item.find_parent("div").find_parent("div")

            availability = StrExt.digits(item.get_text())
            if len(availability) > 0:
                alias_comp = parent.find("h4", class_="product-title").find("a")
                product_title = alias_comp.get_text()            
                sku = product_title.split(" ")[-1].lower()

                parsed = ParsedItem()
                parsed.old_price, parsed.new_price = price_pair(parent)
                parsed.href = alias_comp["href"]
                parsed.sku = sku
                parsed.stock = ParsedItem.Stock.IN_STOCK

                self.items[sku] = parsed
            else:
                self.reaches_end = True
                break
        self.currentPage += 1


# Public methods

    def parse(self):
        while not self.reaches_end:
            self._get_next_page()
        print(len(self.items))