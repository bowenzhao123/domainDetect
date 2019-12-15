
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUGE = False
    TESTING = False
    SECRET_KEY = "12345"
    #SQLALCHEMY_DATABASE_URL = os.environment['DATABASE_URL']

class SelectorConfig:
    brand_name = ''
    brand_link = ''
    phone = ''
    street = ''
    postal = ''

class ParserConfig:
    brand_name = ''
    brand_link = ''
    phone = ''
    street = ''
    postal = ''

class TypesConfig:
    brand_name = ''
    brand_link = ''
    phone = ''
    street = ''
    postal = ''

class FTDStateConfig:
    name_selector = 'ul li.clearfix a[role=link]'
    url_selector = name_selector
    name_parser = lambda x: x.replace("http://www.ftdflorists.com", "").replace("/States/","").replace("%20", " ")
    url_parser = lambda x: 'http://www.ftdflorists.com{}'.format(x)
    save_file = 'data/ftd_state_list.json'

class FTDCityConfig:
    name_selector = 'ul li.clearfix a[role=link]'
    url_selector = name_selector
    name_parser = lambda x: x.split('/')[-1].replace("%20", " ")
    url_parser = lambda x: 'http://www.ftdflorists.com{}'.format(x)
    save_file = 'data/ftd_city_list.json'


class FtdDownloadXpathConfig:
    selector = 'div[class="block-bordered border-radius"]'

class FtdSelectorConfig(SelectorConfig):
    brand_name = 'h3'
    brand_link = 'div.clearfix div button[role=button]'
    street = 'address span'
    phone = 'h3'
    postal = 'address p'

class FtdParserConfig(ParserConfig):
    brand_name = lambda x:x
    brand_link = lambda x: '' if not x else x.replace('window.open', '').replace("('", '').replace("')", '')
    street = lambda x:x 
    phone = lambda x:x 
    postal = lambda x: '' if not x else x.split()[-1]

class FtdTypeConfig(TypesConfig):
    brand_name = 'text'
    brand_link = 'onclick'
    phone = 'text'
    street = 'text'
    postal = 'text'

"""
class BloomNationSelectorConfig(SelectorConfig):
    name = 'h1[class=store_name]'
    url = 'p[class=store_location] span a'
    phone = ''
    street = 'p[class=store_location] a'
    postal = 'p[class=store_location] a'

class TelefloraSelectorConfig(SelectorConfig):
    name = 'h3,h5'
    url = 'a'
    phone = 'span[class=tel]'
    street = 'span[class=street-address]'
    postal = 'span[class=postal-code]'


"""

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
