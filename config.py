class SelectorConfig:
    name = ''
    url = ''
    phone = ''
    street = ''
    postal = ''

class ParserConfig:
    name = ''
    url = ''
    phone = ''
    street = ''
    postal = ''

class TypesConfig:
    name = ''
    url = ''
    phone = ''
    street = ''
    postal = ''


class FtdDownloadXpathConfig:
    selector = 'div[class=block-bordered border-radius]'

class FtdSelectorConfig(SelectorConfig):
    name = 'h3'
    url = 'div.clearfix div button[role=button]'
    street = 'address span'
    phone = 'h3'
    postal = 'address p'

class FtdParserConfig(ParserConfig):
    name = lambda x:x 
    url = lambda x: '' if not x else x.replace('window.open', '').replace("('", '').replace("')", '')
    street = lambda x:x 
    phone = lambda x:x 
    postal = lambda x: '' if not x else x.split()[-1]

class FtdTypeConfig(TypesConfig):
    name = 'text'
    url = 'onclick'
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