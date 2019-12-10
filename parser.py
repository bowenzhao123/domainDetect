

from functools import partial 

class BaseParser:
    def __init__(self,engine):
        self.engine = engine

    def parser(self,response,transform, attr=None):
        if not attr:
            content = response.text
        else:
            content = response.get(attr)
        return partial(transform, content)

    def send_item(self,domain,elements):
        pass

class NameParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_item(self,domain,elements):
        self.engine.get_name_content(domain,elements)
    
class UrlParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_item(self,domain,elements):
        self.engine.get_url_content(domain,elements)

class PhoneParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_item(self,domain,elements):
        self.engine.get_phone_content(domain,elements)

class StreetParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_item(self,domain,elements):
        self.engine.get_street_content(domain,elements)

class PostalParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_item(self,domain,elements):
        self.engine.get_postal_content(domain,elements)
