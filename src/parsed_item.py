from enum import Enum

class ParsedItem:

# Variables

    class Stock(Enum):
        IN_STOCK = 0        
        WAREHOUSE = 1
        OUT_STOCK = 2
        WAITING = 3

        @classmethod
        def get_feed(cls, source):
            result = cls.OUT_STOCK
            match source:
                case "in stock":
                    result = cls.IN_STOCK
                case "preorder":
                    result = cls.WAITING
            return result

    sku = ""
    old_price = 0
    new_price = 0
    href = ""
    stock = Stock.OUT_STOCK


# Delegate methods

    def __eq__(self, value):
        if not isinstance(value, ParsedItem):
            return False
        return self.sku == value.sku
    

    def __hash__(self):
        return hash(self.sku)