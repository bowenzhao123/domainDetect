

from functools import partial 

class BaseParser:
    def __init__(self,engine):
        self.engine = engine

    def extract_content(self,element,transform, attr=None):
        if attr == 'text':
            content = element.text
        else:
            content = element.get(attr)
        return partial(transform, content)

    def send_content_to_engine(self,domain,content):
        pass

class NameParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_content_to_engine(self,domain,content):
        self.engine.get_name_content(domain,content)
    
class UrlParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_content_to_engine(self,domain,content):
        self.engine.get_url_content(domain,content)

class PhoneParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_content_to_engine(self,domain,content):
        self.engine.get_phone_content(domain,content)

class StreetParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_content_to_engine(self,domain,content):
        self.engine.get_street_content(domain,content)

class PostalParser(BaseParser):
    def __init__(self,engine):
        BaseParser.__init__(self,engine)

    def send_content_to_engine(self,domain,content):
        self.engine.get_postal_content(domain,content)
