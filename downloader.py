import requests
import bs4 
from bs4 import BeautifulSoup
from engine import Engine

class BaseDownloader:
    def __init__(self, engine):
        self.engine = engine

    def get_response(self,request):
        page = BeautifulSoup(request.content,'html.parser')
        return page
