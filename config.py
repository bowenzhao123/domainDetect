class XpathConfig:
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

class Types:
    name = ''
    url = ''
    phone = ''
    street = ''
    postal = ''

class FtdXpathConfig(XpathConfig):
    name = 'h3'
    url = 'div.clearfix div button[role=button]'
    street = 'address span'
    phone = 'h3'
    postal = 'address p'

class BloomNationXpathConfig(XpathConfig):
    name = 'h1[class=store_name]'
    url = 'p[class=store_location] span a'
    phone = ''
    street = 'p[class=store_location] a'
    postal = 'p[class=store_location] a'

class TelefloraXpathConfig(XpathConfig):
    name = 'h3,h5'
    url = 'a'
    phone = 'span[class=tel]'
    street = 'span[class=street-address]'
    postal = 'span[class=postal-code]'


class FtdParserConfig(ParserConfig):
    pass