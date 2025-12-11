from enum import Enum

class ParsedItem:

    class Stock(Enum):
        IN_STOCK = 1
        OUT_STOCK = 2
        WAREHOUSE = 3
        WAITING = 4

    sku = ""
    old_price = 0
    new_price = 0
    href = ""
    stock = Stock.OUT_STOCK