class BaseSpider:

    def __init__(self,engine):
        self.engine = engine

    def select_elements(self,response,selector,index):
        if not index:
            elements = response.select(selector)
        else:
            elements = response.select(selector)[:index]
        return elements

    def send_element_to_engine(self,domain,elements):
        pass

class NameSpider(BaseSpider):
    def __init__(self,engine):
        BaseSpider.__init__(self,engine)
    
    def send_element_to_engine(self,domain,elements):
        self.engine.get_name_response((domain,elements))

class UrlSpider(BaseSpider):
    def __init__(self,engine):
        BaseSpider.__init__(self,engine)

    def send_element_to_engine(self, domain,elements):
        self.engine.get_url_response((domain,elements))

class PhoneSpider(BaseSpider):
    def __init__(self,engine):
        BaseSpider.__init__(self,engine)

    def send_element_to_engine(self, domain,elements):
        self.engine.get_phone_response((domain,elements))

class StreetSpider(BaseSpider):
    def __init__(self,engine):
        BaseSpider.__init__(self,engine)

    def send_element_to_engine(self, domain,elements):
        self.engine.get_street_response((domain,elements))

class PostalSpider(BaseSpider):
    def __init__(self,engine):
        BaseSpider.__init__(self,engine)

    def send_element_to_engine(self, domain,elements):
        self.engine.get_postal_response((domain,elements))

