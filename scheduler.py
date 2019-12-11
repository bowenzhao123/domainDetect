
import requests
from engine import Engine

class Scheduler:
    def __init__(self,proxies,headers,engine):
        self.proxies = proxies
        self.headers = headers
        self.engine = engine

    def rotate_proxy(self):
        pass
    
    def rotate_header(self):
        pass
    
    def format_error(self,e):
        return e

    def send_request(self,url,header):
        try:
            redir_url = requests.get(url,verify=False,headers=header).url
            req = requests.get(redir_url,verify=False,headers=header)
            self.engine.get_request((url,req))
        except Exception as e:
            self.engine.error_pool.put((url,self.format_error(e)))

    def get_new_url(self,element,selector):
        new_url = element.select(selector).get('href')
        if new_url:
            return new_url
        return