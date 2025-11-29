import configparser
from src.settings import Settings


config_path = "config.ini"


def main():
    settings = Settings(config_path)
    print(settings.feed.url)
    print(settings.source.page_argument)


if __name__ == "__main__":
    main()