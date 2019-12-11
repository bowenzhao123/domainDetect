
import queue
from queue import Queue

class Engine:
    def __init__(self):

#########################################################
        self._request_pool = Queue()
        self._response_pool = Queue()
        self.error_pool = Queue()

#########################################################
        self._name_spider_pool = Queue()
        self._url_spider_pool = Queue()
        self._phone_spider_pool = Queue()
        self._street_spider_pool = Queue()
        self._postal_spider_pool = Queue()

##########################################################
        self._name_content_pool = Queue()
        self._url_content_pool = Queue()
        self._phone_content_pool = Queue()
        self._street_content_pool = Queue()
        self._postal_content_pool = Queue()    

#############################################################
    def send_request(self):
        if self._request_pool.empty():
            return 
        request = self._request_pool.get()
        return request
    
    def get_request(self,request):
        self._request_pool.put(request)

############################################################
    def send_response(self):
        if self._request_pool.empty():
            return 
        response = self._request_pool.get()
        return response
    
    def get_response(self,domain,response):
        self._response_pool.put((domain,response))

#############################################################
    def get_name_response(self,domain, response):
        self._name_spider_pool.put((domain,response))

    def send_name_response(self):
        if self._name_spider_pool.empty():
            return 
        response = self._name_spider_pool.get()
        return response

    def get_url_response(self,domain, response):
        self._url_spider_pool.put((domain,response))

    def send_url_response(self):
        if self._url_spider_pool.empty():
            return 
        response = self._url_spider_pool.get()
        return response

    def get_phone_response(self,domain,response):
        self._phone_spider_pool.put((domain,response))

    def send_phone_response(self):
        if self._phone_spider_pool.empty():
            return 
        response = self._phone_spider_pool.get()
        return response

    def get_street_response(self,domain,response):
        self._street_spider_pool.put((domain,response))

    def send_street_response(self):
        if self._street_spider_pool.empty():
            return 
        response = self._street_spider_pool.get()
        return response

    def get_postal_response(self,domain,response):
        self._postal_spider_pool.put((domain,response))

    def send_postal_response(self):
        if self._postal_spider_pool.empty():
            return 
        response = self._postal_spider_pool.get()
        return response

######################################################
    def get_name_content(self,domain, response):
        self._name_content_pool.put((domain,response))

    def send_name_content(self):
        if self._name_content_pool.empty():
            return 
        response = self._name_content_pool.get()
        return response

    def get_url_content(self,domain, response):
        self._url_content_pool.put((domain,response))

    def send_url_content(self):
        if self._url_content_pool.empty():
            return 
        response = self._url_content_pool.get()
        return response

    def get_phone_content(self,domain,response):
        self._phone_content_pool.put((domain,response))

    def send_phone_content(self):
        if self._phone_content_pool.empty():
            return 
        response = self._phone_content_pool.get()
        return response

    def get_street_content(self,domain,response):
        self._street_content_pool.put((domain,response))

    def send_street_content(self):
        if self._street_content_pool.empty():
            return 
        response = self._street_content_pool.get()
        return response

    def get_postal_content(self,domain,response):
        self._postal_content_pool.put((domain,response))

    def send_postal_content(self):
        if self._postal_content_pool.empty():
            return 
        response = self._postal_content_pool.get()
        return response

###########################################################