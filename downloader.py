import requests
import bs4 
from bs4 import BeautifulSoup
from engine import Engine

class BaseDownloader:
    def __init__(self, engine):
        self.engine = engine

    def get_response(self,request,selector=''):
        page = BeautifulSoup(request.content,'html.parser')
        if not selector:
            return page
        return page.select(selector)
