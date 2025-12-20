from src.settings import Settings
from src.category_parser import CategoryParser

class SiteParser:

# Instance initialization

    def __init__(self, settings: Settings):
        self.items = dict()
        self._parse(settings)

# Private methods

    def _parse(self, settings: Settings):
        print("Start parsing site items...")
        for category in settings.source.category_pathes:
            category_items = CategoryParser(settings, category)
            self.items[category] = category_items.items
        print(len(self.items))
