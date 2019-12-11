
import queue
from queue import Queue

class FloristInformation:
    def __init__(self,source_url,brand_name,homepage_url,work_phone,shop_street,postal):
        self.source_url = source_url
        self.brand_name = brand_name
        self.homepage_url = homepage_url
        self.work_phone = work_phone
        self.shop_street = shop_street
        self.postal = postal

class FloristInformationPool:
    def __init__(self):
        self.florist_information_pool = Queue()

    def push_florist_information(self,florist_information):
        if not isinstance(florist_information,FloristInformation):
            raise ValueError('')
        self.florist_information_pool.put(florist_information)
    
    def fetch_florist_information(self):
        if self.florist_information_pool.empty():
            return
        return self.florist_information_pool.get()


class Engine:
    def __init__(self):

#########################################################
        self._request_pool = Queue()
        self._response_pool = Queue()
        self._start_url_list = Queue()

        self._florist_html_element_pool = FloristInformationPool()
        self._florist_content_pool = FloristInformationPool()

#############################################################
    def create_start_url_list(self,start_url_lists):
        for url in start_url_lists:
            self._start_url_list.put(url)
    
    def send_url_to_scheduler(self):
        if self._start_url_list.empty():
            return
        url = self._request_pool.get()
        return url

    def get_request_from_scheduler(self,request):
        self._request_pool.put(request)

    def send_request_to_downloader(self):
        if self._request_pool.empty():
            return 
        request = self._request_pool.get()
        return request

    def get_response_from_downloader(self, response):
        self._response_pool.put(response)
    
    def send_response_to_spider(self,url_link,response):
        self._response_pool.put((url_link,response))

    def get_html_element_from_spider(self,florist_html_element):
        self._florist_html_element_pool.push_florist_information(florist_html_element)
    
    def send_html_element_to_parser(self):
        florist_html_element = self._florist_html_element_pool.fetch_florist_information()
        return florist_html_element

    def get_content_from_parser(self,florist_content):
        self._florist_content_pool.push_florist_information(florist_content)

    