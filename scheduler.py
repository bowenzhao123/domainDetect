
import requests
from engine import Engine


class ResponseData:
    
    self.source_url = 
    self.response = 

class Scheduler:
    def __init__(self,proxies,headers,engine):
        self.proxies = proxies
        self.headers = headers

    def rotate_proxy(self):
        pass
    
    def rotate_header(self):
        pass
    
    def format_error(self,e):
        return e

    def send_request(self,url,header):
        try:
            redir_url = requests.get(url,verify=False,headers=header).url
            response = requests.get(redir_url,verify=False,headers=header)
            return response
        except Exception as e:
            print(self.format_error(e))
            return

    def get_next_page_link(self,element,next_page_element_selector):
        new_url = element.select(next_page_element_selector).get('href')
        if new_url:
            return new_url
        return