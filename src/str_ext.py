import re

class StrExt:

    @classmethod
    def digits(cls, source):
        return "".join(filter(str.isdigit, source))
    
    @classmethod
    def split(cls, source):
        return re.sub(r'[\t\n\r]', '', source)
