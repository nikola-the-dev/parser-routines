import configparser
from src.settings import Settings
from src.feed_parser import FeedParser
from src.site_parser import SiteParser


config_path = "./ignore/config.ini"


def main():
    settings = Settings(config_path)
    feed_parser = FeedParser(settings)
    site_parser = SiteParser(settings)

if __name__ == "__main__":
    main()