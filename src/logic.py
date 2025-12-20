from src.feed_parser import FeedParser
from src.site_parser import SiteParser
from src.settings import Settings
from src.parsed_item import ParsedItem
import csv


def compose(feed: FeedParser, site: SiteParser, settings: Settings):
    print("Start forming output files...")
    output = settings.output
    items = [[output.sku_col_name, output.stock_col_name]]
    new_items = [[output.sku_col_name, "URL"]]

    def stock(code):
        if code < len(output.stock_names):
            return output.stock_names[code]        
        return output.stock_names[-1]

    for category in settings.source.category_pathes:
        print(f"Forming data for {category}")
        feed_items: FeedParser.Item = feed.items[category]
        site_items = site.items[category]
        warehouse_items = feed_items.absence_items & site_items
        out_stock_items = feed_items.absence_items - warehouse_items
        missed_items = site_items - feed_items.all_items()
        items.extend([[feed.map_ids[item.sku], stock(ParsedItem.Stock.WAREHOUSE.value)] for item in warehouse_items])
        items.extend([[feed.map_ids[item.sku], stock(ParsedItem.Stock.OUT_STOCK.value)] for item in out_stock_items])
        new_items.extend([[item.sku, item.href] for item in missed_items])
    
    def write_file(path, data):
        print(f"Writing {path}...")
        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    write_file("items.csv", items)
    write_file("items_new.csv", new_items)
    print("Finish writing files")
    
