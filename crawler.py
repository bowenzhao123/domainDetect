#!/usr/bin/env python
from __future__ import print_function
import os
import requests
import time
from collections import defaultdict
import json
import selenium
from selenium import webdriver
import re
import socket
from selenium.common.exceptions import NoSuchElementException
#from . import *
import sys
sys.path.append('..')
import json
import csv
# import config

class Crawlers:
    
    DomainInfo = {
        "ftdSearchDomain":"http://www.ftdflorists.com",
        "bloomNationSearchDomain":"https://www.bloomnation.com/flower-delivery-cities/",
        "telefloraSearchDomain":"http://www.findaflorist.com/sitemap.aspx",
        "bloomNetSearchDomain":"http://www.locatemyflorist.com/find-florists-by-state/",
        "bloomNetDomain":"http://www.locatemyflorist.com",
        "fsnSearchDomain":"https://www.flowershopnetwork.com/florists/",
        "fsnDomain":"https://www.flowershopnetwork.com"
    },
    
    recoverIndex = {
        "ftd":0,
        "bloomNation":0,
        "bloomNet":0,
        "fsn":0,
        "teleflora":0
    },
    stateList = {
        "ftd":None,
        "bloomNation":None,
        "bloomNet":None,
        "fsn":None,
        "teleflora":None
    },
    stateUrl = {
        "ftd":None,
        "bloomNation":None,
        "bloomNet":None,
        "fsn":None,
        "teleflora":None
    },
    clean = False,
    prov_ns = {"teleflora": "eflorist.com", "ftd": "ftd.com", "floristboard": "iflorists.org",
                    "bloomNation":"", "fsn":"",
                   "rkfhosting": "rkfhosting.com", "locateaflowershop": "lafscom.net",
                   "webshop101": "webshop101.com", "media99": "media99.com", "websystems": "websystems.com" },
    stateMapper = {"Alaska": "AK",
        "Alabama": "AL",
        "Arkansas": "AR",
        "American Samoa": "AS",
        "Arizona": "AZ",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "District of Columbia": "DC",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Guam": "GU",
        "Hawaii": "HI",
        "Iowa": "IA",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Massachusetts": "MA",
        "Maryland": "MD",
        "Maine": "ME",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Missouri": "MO",
        "Northern Mariana Islands": "MP",
        "Mississippi": "MS",
        "Montana": "MT",
        "National": "NA",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Nebraska": "NE",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "Nevada": "NV",
        "New York": "NY",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Puerto Rico": "PR",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Virginia": "VA",
        "Virgin Islands": "VI",
        "Vermont": "VT",
        "Washington": "WA",
        "Wisconsin": "WI",
        "West Virginia": "WV",
        "Wyoming": "WY"
        }

    def __init__(self,env):
        #self._conf = getattr(config, env.title())
        #self._domainUrl = '{}/domains/'.format(self._conf.DOMAIN)
        #self._contactUrl = '{}/contacts/'.format(self._conf.DOMAIN)
        #print(self._domainUrl)
        #print(self._contactUrl)
        pass

    def _handelError(self,url):
        try:
            r = requests.get(url, timeout=3)
            return r.status_code
        except:
            print("requests error")
            return 404

    def _modifyBody(self,body,provider):
        """ given a url, create domain name, ip, status, type
        body example:
            {
                'domain_name': 'https://wwww.bestflowerist.com'
            }
        output example:
            {
                'domain_name':'wwww.bestflowerist.com',
                'https':1,
                'status':200,
                'ip':127.000.000.000
                'type':'web'
            }
        """
        domainName = body["domain_name"]
        body["type"] = "web"
        try:
            status = self._handelError(domainName)
        except:
            status = 404

        body["status"] = status

        https = 1 if ("https" in domainName or "HTTPS" in domainName) else 0

        body["https"] = https
        
        domainName = domainName.replace("https://","").replace("http://","").replace("HTTPS://","").replace("HTTP://","").replace("www.","")
        if domainName and domainName[-1] in ("?/"):
            domainName = domainName[:-1]
        
        body["domain_name"] = domainName
        
        #try:
        #    ip = socket.gethostbyname(domainName)
        #    body["ip"] = ip
        #except:
        #    pass
        
        
        body["provider"] = provider
        body["nameservers"] = [Crawlers.prov_ns[0][provider]]
        return body

    def _createDriver(self):
        """ create a selenium phantomjs driver
        """
        driver = webdriver.PhantomJS(service_args=["--load-images=no"])
        driver.implicitly_wait(5)
        driver.set_page_load_timeout(5)
        return driver
    
    def _openBrowser(self,driver,url,timesleep=5):
        """ open browser
        """
        try:
            driver.get(url)
            time.sleep(1)
        except Exception as e:
            print(e)


    def _findElement(self,element, xpath, types, index=0):
        """ given a crawler role, and content type, element node, return the content
        example:
            xpath:'//div[@class="clearfix"]/div/button[@role="button"]'
            types: 'href'
            index: 2 
        """
        try:
            if xpath and index == 0:
                element = element.find_element_by_xpath(xpath)
            if xpath and index > 0:
                element = element.find_elements_by_xpath(xpath)[index]
            if types == "text":
                return element.text
            else:
                return element.get_attribute(types)
        except NoSuchElementException:
            print("NoSuchElement")
        return

    def _findAllElements(self,element, xpath, types, filters, parsers):
        """ find all elements that satisfy the crawler rules
        example:
            "xpath": "//h3", 
            "types": "text", 
            "parser": lambda x: x, 
            "filters": lambda x: x and x.text
        """
        try:
            newelement = element.find_elements_by_xpath(xpath) if xpath else element
            if types == "text":
                newelement = list(filter(lambda x:x and x.text, newelement))
                newelement = list(map(lambda x:x.text, newelement))
            else:
                newelement = list(filter(lambda x:x and x.get_attribute(types), newelement))
                newelement = list(map(lambda x:x.get_attribute(types), newelement))
            if filters:
                newelement = list(filter(filters,newelement))
            if parsers:
                newelement = list(map(parsers,newelement))
            return newelement
        except NoSuchElementException:
            print("NoSuchElement")
        return

    def _getNameUrlList(self,driver,url,xpath,parseUrl,parseText,nameType,urlType,blockList,urlxpath=None,namexpath=None):
        """ Get all the content and links
        example:
           "xpath": '//li[@class="clearfix"]/a',
            "parseText": lambda x: x.replace("http://www.ftdflorists.com/States/", "").replace("%20", " "), # get the content
            "parseUrl": lambda x:x.get_attribute('href'),  # get the url
            "nameType": "href",  #  url
            "urlType": "href", #  name
            "blockList": [] # the website to block 
        """
        self._openBrowser(driver,url)
        names = []
        urls = []
        for link in driver.find_elements_by_xpath(xpath):
            try:
                url = self._findElement(link,xpath=urlxpath,types=urlType)
                name = self._findElement(link,xpath=namexpath,types=nameType)
                if parseUrl:
                    url = list(map(parseUrl,[name]))[0]
                if parseText:
                    name = list(map(parseText,[name]))[0]
                if name in blockList:
                    break
                if name in names:
                    continue
                names.append(name)
                urls.append(url)
            except:
                continue
        return names, urls

    def _getStateUrl(self,driver,url,xpath,parseUrl,parseText,nameType,urlType, blockList,urlxpath=None,namexpath=None):
        """ a wrapper of getNameUrlList function, used to get state url and name
        """
        if self._recoverIndex != 0 and self._recoverIndex < (len(self._stateList) - 1):
            #print "recover from the disrupt!"
            print("start from: {}".format(self._stateList[self._recoverIndex]))
        elif not self._stateList:
            self._stateList,self._stateUrl = self._getNameUrlList(driver,url,xpath,parseUrl,parseText,nameType,urlType, blockList,urlxpath,namexpath)
        else:
            return
    

#    def _addData(self, data, url):
#        """  write the data into database
#        """
#        res = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json'},verify=False)
#        return res

    def _createBodyInfo(self,obj,body,element):
        """ create the data that will be loaded into database in the furture
        body: initialized data
        element: element node
        obj:  # crawlering and parsing rules, key is field of data ('name','phone','street',..), value including: crawler rules, filter rules, and parsing rules
            {
            "company_name": {"xpath": "//h3", "types": "text", "parser": lambda x: x, "index": 0},
            "street1": {"xpath": '//address/span', "types": "text", "parser": lambda x: x, "index": 0},
            "phone": {"xpath": "//h3", "types": "text", "parser": lambda x: x, "index": 1},
            "postal": {"xpath": "//address/p", "types": "text", "parser": lambda x: x.split()[-1], "index": 0} 
            }
        """
        for field, val in obj.items():
            try:
                res = self._findElement(element,val["xpath"],val["types"],val["index"])
                parser = val["parser"]
                if res and list(map(parser,[res]))[0]:
                    res = list(map(parser,[res]))[0]
                    body[field] = res
            except:
                continue
        return body

    def _getFtdShops(self):
        """ get ftd's flower shops
        """
        self._rootUrl = Crawlers.DomainInfo[0]["ftdSearchDomain"] 
        self._stateList = Crawlers.stateList[0]["ftd"]
        self._stateUrl = Crawlers.stateUrl[0]["ftd"]
        self._recoverIndex = Crawlers.recoverIndex[0]["ftd"]  # where to start if the process is interupted 
        # rules of getting states name and urls
        self.stateRuleSet = {
            "xpath": '//li[@class="clearfix"]/a',
            "parseText": lambda x: x.replace("http://www.ftdflorists.com/States/", "").replace("%20", " "),
            "parseUrl": None,
            "nameType": "href",
            "urlType": "href",
            "blockList": []
        }
        # rules of getting city name and urls
        self.cityRuleSet = {
            "xpath": '//div[@class="clearfix state-results"]//li/a',
            "parseUrl": None,
            "nameType": "href",
            "urlType": "href",
            "blockList": ["/States/Alabama"]
        }
        # rules of screening contacts information
        self.obj_address = {
            "company_name": {"xpath": "//h3", "types": "text", "parser": lambda x: x, "index": 0},
            "street1": {"xpath": '//address/span', "types": "text", "parser": lambda x: x, "index": 0},
            "phone": {"xpath": "//h3", "types": "text", "parser": lambda x: x, "index": 1},
            "postal": {"xpath": "//address/p", "types": "text", "parser": lambda x: x.split()[-1], "index": 0}
        }
        # rules of screening domain information
        self.domain_para = {"xpath": '//div[@class="clearfix"]/div/button[@role="button"]', "types": "onclick", "index": 0}
        
        url = "{}/States".format(self._rootUrl)
        self._handelError(url)
        driver = self._createDriver()
        self._getStateUrl(driver, url, **self.stateRuleSet)
        # get all state url and names
        self._stateList = list(map(lambda x:Crawlers.stateMapper.get(x),self._stateList))

        newdriver = self._createDriver()
        for i in range(self._recoverIndex, len(self._stateList)):
            parseText = lambda x: x.replace(self._stateUrl[i] + "/", "").replace("%20", " ")
            # get all city url and names within the given state
            cityNames, cityLists = self._getNameUrlList(driver, self._stateUrl[i],parseText=parseText, **self.cityRuleSet)
            for cityName, cityList in zip(cityNames, cityLists):
                # get all the partners' information within the given city
                self._openBrowser(newdriver, cityList)
                contacts = defaultdict()
                contacts["state"] = self._stateList[i].upper()
                if cityName:
                    contacts["city"] = cityName
                for element in newdriver.find_elements_by_xpath('//div[@class="block-bordered border-radius"]'):
                    contacts = dict(self._createBodyInfo(self.obj_address, contacts, element))
                    domain = self._findElement(element, **self.domain_para)
                    try:
                        # create the shops' information
                        domainName = domain.replace('window.open', '').replace("('", '').replace("')", '')
                        domainBody = defaultdict()
                        domainBody["domain_name"] = domainName
                        domainBody = dict(self._modifyBody(domainBody,"ftd"))
                        contacts["domain_name"] = domainBody["domain_name"]
                        # write to the database
                        res = requests.post('http://0.0.0.0:5001/domains/', data=json.dumps(domainBody), headers={'content-type': 'application/json'},verify=False)
                        print(res)
                        time.sleep(2)
                        res = requests.post('http://0.0.0.0:5001/contacts/',data=json.dumps(contacts), headers={'content-type': 'application/json'},verify=False)
                        print(res)
                        time.sleep(2)
                    except:
                        continue
            self._recoverIndex = i
        newdriver.quit()
        driver.quit()

    def _getBloomNationShops(self):
        self._rootUrl = Crawlers.DomainInfo[0]['bloomNationSearchDomain']
        self._stateList = Crawlers.stateList[0]['bloomNation']
        self._stateUrl = Crawlers.stateUrl[0]['bloomNation']
        self._recoverIndex = Crawlers.recoverIndex[0]['bloomNation']

        self.stateRuleSet = {
            'xpath': '//div[@class="state"]',
            'urlxpath': 'ul/li[@class="topcities-seemore"]/a',
            'namexpath': 'div[@class="stateName"]',
            'parseText': None,
            'parseUrl': None,
            'nameType': 'text',
            'urlType': 'href',
            'blockList': []
        }
        self.cityRuleSet = {
            'xpath': '//div[@class="col-list"]//li/a',
            'parseUrl': None,
            'nameType': 'text',
            'urlType': 'href',
            'blockList': []
        }
        self.obj_address = {
            'company_name':{'xpath':'//h1[@class="store_name"]','types':'text','parser':lambda x:x,'index':0},
            'street1':{'xpath':'//p[@class="store_location"]/a','types':'href','parser': lambda x:x.replace(
                                        'https://www.google.com/maps/dir/Current+Location/', '').split(',')[0].replace('%20', ' '),'index':0},
            'postal':{'xpath':'//p[@class="store_location"]/a','types':'href','parser': lambda x:x.replace(
                                        'https://www.google.com/maps/dir/Current+Location/', '').split(',')[0].replace('%20', ''),'index':0}
        }
        self.domain_para = {}
        url = self._rootUrl
        self._handelError(url)
        driver = self._createDriver()

        self._getStateUrl(driver,url, **self.stateRuleSet)
        newdriver = self._createDriver()
        for i in range(self._recoverIndex, len(self._stateList)):
            parseText = lambda x: x.replace(self._stateUrl[i] + '/', '').replace('%20', ' ')
            cityNames, cityLists = self._getNameUrlList(driver, self._stateUrl[i], parseText=parseText, **self.cityRuleSet)
            for city, cityUrl in zip(cityNames, cityLists):
                shopUrlLs = set()
                currentPageUrl = cityUrl
                self._openBrowser(newdriver, cityUrl, timesleep=2)
                # click-on to the next page, and gather all the distinct partners
                while currentPageUrl:
                    try:
                        for shopLink in newdriver.find_elements_by_xpath('//h2[@class="product_florist"]/a'):
                            try:
                                shopRedirect = shopLink.get_attribute('href')
                                if shopRedirect in shopUrlLs:
                                    continue
                                shopUrlLs.add(shopRedirect)
                            except:
                                continue
                        currentPageUrl = newdriver.find_element_by_xpath('//footer//a[@class="next-link"]').get_attribute('href')
                        self._openBrowser(driver, currentPageUrl, timesleep=3)
                    except:
                        break
                # get all the partners' information, given a list of urls
                for url in shopUrlLs:
                    self._openBrowser(newdriver, url)
                    contacts = defaultdict()
                    contacts['state'] = self._stateList[i].upper()
                    if city:
                        contacts['city'] = city
                    contacts = dict(self._createBodyInfo(self.obj_address, contacts, newdriver))
                    try:
                        domainName = newdriver.find_element_by_xpath('//p[@class="store_location"]/span/a')
                        if domainName.get_attribute('href'):
                            domainName = domainName.get_attribute('href')
                        elif domainName.text:
                            domainName = domainName.text
                        else:
                            continue
                        # write to the database
                        domainBody = defaultdict()
                        domainBody['domain_name'] = domainName
                        domainBody = dict(self._modifyBody(domainBody,'bloomNation'))
                        contacts['domain_name'] = domainBody['domain_name']
                        res = requests.post('http://0.0.0.0:5001/domains/', data=json.dumps(domainBody), headers={'content-type': 'application/json'},verify=False)
                        print(res)
                        time.sleep(2)
                        res = requests.post('http://0.0.0.0:5001/contacts/',data=json.dumps(contacts), headers={'content-type': 'application/json'},verify=False)
                        print(res)
                        time.sleep(2)
                    except:
                        continue
            self._recoverIndex = i
        newdriver.quit()
        driver.quit()
    
    def _getTelefloraShops(self):
        self._stateList = Crawlers.stateList[0]['teleflora']
        self._stateUrl = Crawlers.stateUrl[0]['teleflora']
        self._recoverIndex = Crawlers.recoverIndex[0]['teleflora']
        self._rootUrl = Crawlers.DomainInfo[0]['telefloraSearchDomain']
        self.stateRuleSet = {
            'xpath': '//a[@class="view-states-link"]',
            'urlxpath': None,
            'namexpath': None,
            'parseText': lambda x:Crawlers.stateMapper.get(x.replace(' Florists','')),
            #'parseText': None,
            'parseUrl': None,
            'nameType': 'text',
            'urlType': 'href',
            'blockList': []
        }
        self.cityRuleSet = {}
        self.cityNameRuleSet = {
            'xpath': '//a[@class="state-city-link"]',
            'types': 'text',
            'parsers': lambda x: x.replace(' Florists', ''),
            'filters': None
        }
        self.cityUrlRuleSet = {
            'xpath': '//a[@class="state-city-link"]',
            'types': 'href',
            'parsers': None,
            'filters': None
        }
        self.obj_address = {
            'company_name': {'xpath': '//h3', 'types': 'text', 'parser': lambda x: x, 'index': 0},
            'phone': {'xpath': '//span[@class="tel"]', 'types': 'text', 'parser': lambda x: x, 'index': 0},
            'street1': {'xpath': '//span[@class="street-address"]', 'types': 'text', 'parser': lambda x: x, 'index': 0},
            'postal': {'xpath': '//span[@class="postal-code"]', 'types': 'text', 'parser': lambda x: x, 'index': 0}
        }
        self.obj_address2 = {
            'company_name': {'xpath': '//h5', 'types': 'text', 'parser': lambda x: x, 'index': 0}
        }
        self.obj_domain = {
            'xpath': '//a',
            'types': 'href',
            'filters': lambda x: x and not x.startswith('http://www.findaflorist.com') and not x.startswith(
                'http://www.telefloraflorist.com') and not x.startswith('http://m.findaflorist.com') and re.match(
                r'(.*)(\?)', x),
            'parsers': lambda x: re.match(r'(.*)(\?)', x).group(0).replace('?', '')
        }

        url = self._rootUrl
        # cls.reset()
        self._handelError(url)
        driver = self._createDriver()
        newdriver = self._createDriver()
        newnewdriver = self._createDriver()
        self._getStateUrl(driver, url, **self.stateRuleSet)
        
        for i in range(4, len(self._stateList)):
            print("state: {}".format(self._stateList[i]))
            self._openBrowser(driver, self._stateUrl[i], timesleep=2)
            for link in driver.find_elements_by_xpath('//div[@class="letter-links-green"]/a')[7:]:
                print(link.get_attribute('href'))
                self._openBrowser(newdriver, link.get_attribute('href'), timesleep=2)
                cityNames = self._findAllElements(newdriver, **self.cityNameRuleSet)
                cityLists = self._findAllElements(newdriver, **self.cityUrlRuleSet)
                domainNames = set()
                #for j in range(20, len(cityNames)):
                    #city, cityList = cityNames[j], cityLists[i]
                for city, cityList in zip(cityNames, cityLists):
                    #print('city index: {}'.format(j))
                    #print(city)
                    self._openBrowser(newnewdriver, cityList, timesleep=2)
                    # there are two types of layout 
                    left = newnewdriver.find_elements_by_xpath('//div[@class="fea_inner_content"]')
                    right = newnewdriver.find_elements_by_xpath('//div[@class="moreShops vcard"]')
                    print(len(left),len(right))
                    if left and right:
                        total = left.extend(right)
                    else:
                        total = left if left else right
                    shopNames = set()
                    try:
                        for shopLink in total:
                            contacts = defaultdict()
                            contacts['state'] = self._stateList[i].upper()
                            if city:
                                contacts['city'] = city
                            contacts = self._createBodyInfo(self.obj_address, contacts, shopLink)
                            if not contacts['company_name']:
                                contacts = dict(self._createBodyInfo(self.obj_address2, contacts, shopLink))
                                print(contacts)
                            domain = self._findAllElements(shopLink, **self.obj_domain)

                            print(domain)

                            if not domain or domain[0] in domainNames:
                                continue
                            domainName = domain[0]
                            domainBody = defaultdict()
                            domainBody['domain_name'] = domainName
                            domainBody = dict(self._modifyBody(domainBody,'teleflora'))
                            contacts['domain_name'] = domainBody['domain_name']
                            print(domainBody)
                            #self._addData(dict(domainBody),'http://0.0.0.0:5000/domains/')
                            res = requests.post('http://0.0.0.0:5001/domains/', data=json.dumps(domainBody), headers={'content-type': 'application/json'},verify=False)
                            print(res)
                            time.sleep(2)
                            res = requests.post('http://0.0.0.0:5001/contacts/',data=json.dumps(contacts), headers={'content-type': 'application/json'},verify=False)
                            print(res)
                            time.sleep(2)
                            domainNames.add(domainName)
                    except:
                        print('no shop found!')
            self._recoverIndex = i
            print("stop by:  {}:".format(i))
        newnewdriver.quit()
        newdriver.quit()
        driver.quit()
        
    def _getFsnShops(self):
        self._rootUrl = Crawlers.DomainInfo[0]['fsnSearchDomain']
        self._stateList = Crawlers.stateList[0]['fsn']
        self._stateUrl = Crawlers.stateUrl[0]['fsn']
        self._recoverIndex = Crawlers.recoverIndex[0]['fsn']
        Crawlers.clean = True
        self.stateRuleSet = {
            'xpath': '//a[@class="state-link"]',
            'urlxpath': None,
            'namexpath': None,
            'parseText': lambda x: (x.split('/')[-1], x.split('/')[-2]),
            'parseUrl': None,
            'nameType': 'href',
            'urlType': 'href',
            'blockList': []
        }
        self.cityRuleSet = {
            'xpath': '//ul[@class="group-column"]/li/a',
            'parseUrl': None,
            'nameType': 'text',
            'urlType': 'href',
            'blockList': [],
            'parseText': None
        }
        self.obj_address = {
            'company_name': {'xpath': '//h3[@class="name"]/a', 'types': 'text',
                             'parser': lambda x: x.replace('\n', '').replace('\t', ''), 'index': 0},
            'street1': {'xpath': '//div[@class="street"]', 'types': 'text', 'parser': lambda x: x, 'index': 0},
            'postal': {'xpath': '//div[@class="city"]', 'types': 'text', 'parser': lambda x: x.split()[-1], 'index': 0}
        }
        self.domain_para = {}
        url = self._rootUrl
        # cls.reset()
        self._handelError(url)
        driver = self._createDriver()
        newdriver = self._createDriver()
        self._getStateUrl(driver, url, **self.stateRuleSet)
        if Crawlers.clean:
            res = list(filter(lambda x: x[0][1] in ['USA', 'CA'], zip(self._stateList, self._stateUrl)))
            self._stateList = list(map(lambda x: x[0][0], res))
            self._stateUrl = list(map(lambda x: x[1], res))
            Crawlers.clean = False
        for i in range(self._recoverIndex, len(self._stateList)):
            cityNames, cityLists = self._getNameUrlList(driver, self._stateUrl[i], **self.cityRuleSet)
            for city, cityUrl in zip(cityNames, cityLists):
                self._openBrowser(newdriver, cityUrl, timesleep=2)
                shopNames = set()
                domainNames = set()
                shopLinks = newdriver.find_elements_by_xpath('//div[@class="premium listing"]')
                for j, shopLink in enumerate(shopLinks):
                    contacts = defaultdict()
                    contacts['state'] = self._stateList[i].upper()
                    if city:
                        contacts['city'] = city
                    self.obj_address['company_name']['index'] = self.obj_address['street1']['index'] = self.obj_address['postal']['index'] = j
                    contacts = self._createBodyInfo(self.obj_address, contacts, shopLink)
                    # each partner may have 1 or 2 websites
                    try:
                        # this type of website needs to be redirected
                        domainName = shopLink.find_elements_by_xpath('//h3[@class="name"]/a')[j].get_attribute('href')
                        time.sleep(5)
                        try:
                            domainName = requests.get(domainName).url
                        except:
                            print('cannot redirect')
                        domainBody = defaultdict()
                        domainBody['domain_name'] = domainName
                        domainBody = self._modifyBody(domainBody,'fsn')
                        contacts['domain_name'] = domainBody['domain_name']
                        print(domainBody)
                        #self._addData(dict(domainBody),self._domainUrl)
                        res = requests.post('http://0.0.0.0:5001/domains/', data=json.dumps(domainBody), headers={'content-type': 'application/json'},verify=False)
                        print(res)
                        time.sleep(2)
                        res = requests.post('http://0.0.0.0:5001/contacts/',data=json.dumps(contacts), headers={'content-type': 'application/json'},verify=False)
                        print(res)
                        time.sleep(2)
                    except:
                        pass
                        
                    try:
                        domainName = shopLink.find_elements_by_xpath('//a[@class="website button n1"]')[j].get_attribute('href')
                        domainBody = defaultdict()
                        domainBody['domain_name'] = domainName
                        domainBody = self._modifyBody(domainBody,'fsn')
                        contacts['domain_name'] = domainBody['domain_name']
                        self._addData(dict(domainBody),self._domainUrl)
                        time.sleep(5)
                        self.__addData(dict(contacts),self._contactUrl)
                        time.sleep(5)
                    except:
                        pass                         
            self._recoverIndex = i
        newdriver.quit()
        driver.quit()

    def runCralwer(self,name):
        funcMap = {
            'ftd':self._getFtdShops,
            'bloomNation':self._getBloomNationShops,
            'teleflora':self._getTelefloraShops,
            'fsn':self._getFsnShops
        }
        func = funcMap.get(name)
        if not func:
            return
        func()
        print('success!')

if __name__ == '__main__':
    crawl = Crawlers('development')
    # print(Crawlers.stateList)
    crawl.runCralwer('teleflora')