from src.feed_parser import FeedParser
from src.site_parser import SiteParser
from src.settings import Settings
from src.parsed_item import ParsedItem
import csv


def compose(feed: FeedParser, site: SiteParser, settings: Settings):
    print("Start forming output files...")
    warehouse_items = feed.absence_items & site.items
    out_stock_items = feed.absence_items - warehouse_items
    missed_items = site.items - feed.all_items

    output = settings.output

    def stock(code):
        if code < len(output.stock_names):
            return output.stock_names[code]        
        return output.stock_names[-1]

    def write_file(path, data):
        print(f"Writing {path}...")
        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    items = [[output.sku_col_name, output.stock_col_name]]
    items.extend([[feed.map_ids[item.sku], stock(ParsedItem.Stock.WAREHOUSE.value)] for item in warehouse_items])
    items.extend([[feed.map_ids[item.sku], stock(ParsedItem.Stock.OUT_STOCK.value)] for item in out_stock_items])
    write_file(f"{settings.source.category_path}.csv", items)

    items = [[output.sku_col_name, "url"]]
    items.extend([[item.sku, item.href] for item in missed_items])
    write_file(f"{settings.source.category_path}_new.csv", items)
    
