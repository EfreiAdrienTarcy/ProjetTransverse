
import os
import json
import ssl
from urllib import response

import requests

from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

from mkmsdk.mkm import Mkm
from mkmsdk.api_map import _API_MAP

from bs4 import BeautifulSoup

os.environ['MKM_APP_TOKEN'] = 'ELwCFTse0F5hLf5R'
os.environ['MKM_APP_SECRET'] = 'lL5RalXOXdG0wvscfNDgd097oYSgblcf'

os.environ['MKM_ACCESS_TOKEN'] =''
os.environ['MKM_ACCESS_TOKEN_SECRET'] =''

user_id = 'ADTARCY'

mkm_sandbox = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_sandbox_root"])

#all_games = mkm_sandbox.market_place.games()
exemple_product = mkm_sandbox.market_place.product(product=361648)


#print(all_games.json())
#print(exemple_product.json())


exemple_find = mkm_sandbox.market_place.find_product(params={"search":"MRD-000","idGame":3,"idLanguage":1})

if exemple_find.status_code == 200:
    print(json.dumps(exemple_find.json(),indent=1))
else:
    print('error bad request')
    print(exemple_find.status_code)
    print(exemple_find.json())


'''
Pour les requetes sur les cartes YuGiOh :
idGame = 3

Pour la langue des cartes :
Anglais : idLanguage = 1
Francais : idLanguage = 2
'''


product_id = exemple_find.json().pop('product')[0].pop('idProduct')

exemple_product = mkm_sandbox.market_place.product(product=product_id)

tmp = exemple_product.json().pop('product')
tmp_price_guide = tmp.pop('priceGuide')

print('idProduct')
print(tmp.get('idProduct'))

print('\nenName')
print(tmp.get('enName'))

print('\nfrName')
print(tmp.get('localization')[1].get('name'))

print('\nimageURL')
print(tmp.get('image'))

print('\nprice_average')
print(tmp_price_guide.get('AVG'))

print('\nsellprice')
print(tmp_price_guide.get('SELL'))

print('\nselltrend')
print(tmp_price_guide.get('TREND'))

'''
expansion_test = mkm_sandbox.market_place.expansions(game=3)
tmp = expansion_test.json()

exp_object = tmp.pop('expansion')[0]

print(exp_object.pop('enName'))
print(exp_object.pop('abbreviation'))


single_test = mkm_sandbox.market_place.expansion_singles(expansion='Dark Revelation 4')
print(single_test.json())
'''