import re

class StrExt:

    @classmethod
    def digits(cls, source):
        return "".join(filter(str.isdigit, source))
    

    @classmethod
    def split(cls, source):
        return re.sub(r'[\t\n\r]', '', source)
    

    @classmethod
    def split_to_list(cls, source: str, is_lower = False):
        if is_lower:
            return cls.split_to_list_lower(source)
        return [item.strip() for item in source.split(",")] 
    

    @classmethod
    def split_to_list_lower(cls, source: str):
        return [item.strip() for item in source.lower().split(",")] 
