
import queue
from queue import Queue
from collections import deque
import requests
import bs4 
from bs4 import BeautifulSoup
from engine import Engine
from config import *
import json
from flask import request
from app import app
import config
from config import *
import time

class FloristInformation:
    def __init__(self,brand_name=None,brand_link=None,phone=None,street=None,postal=None):
        self.brand_name = brand_name
        self.brand_link = brand_link
        self.phone = phone
        self.street = street
        self.postal = postal

class Engine:
    def __init__(self):
        self.start_url_list = deque()
        self.request = None
        self.response = deque()
        self.florist_html_element = deque()
        self.florist_content = deque()

def create_request(url):
    try:
        redir_url = requests.get(url, verify=False).url
        response = requests.get(redir_url, verify=False)
        return response
    except Exception as e:
        return

def run_scheduler(engine):
    url = engine.start_url_list.popleft()
    req = create_request(url)
    engine.request.append(req)

def create_response(req,selector=None):
    page = BeautifulSoup(req.content,'html.parser')
    if not selector:
        return page
    return page.select(selector)

def run_ftd_downloader(engine):
    req = engine.request.popleft()
    responses = create_response(req,FtdDownloadXpathConfig.selector)
    print(len(responses))
    for response in responses:
        engine.response.append(response)

def select_elements(response,selector,index=0):
    elements = response.select(selector)[index]
    return elements

def create_html_element(response):
    brand_name_element = select_elements(response,FtdSelectorConfig.brand_name)
    brand_link_element = select_elements(response,FtdSelectorConfig.brand_link)
    phone_element = select_elements(response,FtdSelectorConfig.phone)
    street_element = select_elements(response,FtdSelectorConfig.street)
    postal_element = select_elements(response,FtdSelectorConfig.postal)
    return FloristInformation(brand_name_element,brand_link_element,phone_element,street_element,postal_element)

def run_spider(engine):
    while True:
        try:
            response = engine.response.popleft()
            html_element = create_html_element(response)
            engine.florist_html_element.append(html_element)
        except Exception as e:
            print('spider',e)
            break

def extract_content(html_element,transform_func, attr=None):
    if attr == 'text':
        content = html_element.text
    else:
        content = html_element.get(attr)
    return transform_func(content)

def create_content(html_element):
    if not isinstance(html_element,FloristInformation):
        raise TypeError('')
    florist_brand_name = extract_content(html_element.brand_name,FtdParserConfig.brand_name,FtdTypeConfig.brand_name)
    florist_brand_link = extract_content(html_element.brand_link,FtdParserConfig.brand_link,FtdTypeConfig.brand_link)
    florist_phone = extract_content(html_element.phone,FtdParserConfig.phone,FtdTypeConfig.phone)
    florist_street = extract_content(html_element.street,FtdParserConfig.street,FtdTypeConfig.street)
    florist_postal = extract_content(html_element.postal,FtdParserConfig.postal,FtdTypeConfig.postal)
    return FloristInformation(florist_brand_name,florist_brand_link,florist_phone,florist_street,florist_postal)

def run_parser(engine):
    while True:
        try:
            html_element = engine.florist_html_element.popleft()
            florist_content = create_content(html_element)
            engine.florist_content.append(florist_content)
        except Exception as e:
            print('parser',e)
            break