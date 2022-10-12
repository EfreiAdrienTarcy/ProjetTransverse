
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

api_url = "https://sandbox.cardmarket.com/ws/v2.0/"
get_games = api_url + "output.json/games"
get_article = api_url + "output.json/articles/:"
get_product = api_url + "output.json/products/find:"

test_request = "https://api.cardmarket.com/ws/v2.0/products/find?search=Springleaf&idGame=1&idLanguage=1"

app_token = 'ELwCFTse0F5hLf5R'
app_secret = 'lL5RalXOXdG0wvscfNDgd097oYSgblcf'

access_token = ''
access_token_secret = ''

os.environ['MKM_APP_TOKEN'] = 'ELwCFTse0F5hLf5R'
os.environ['MKM_APP_SECRET'] = 'lL5RalXOXdG0wvscfNDgd097oYSgblcf'

os.environ['MKM_ACCESS_TOKEN'] =''
os.environ['MKM_ACCESS_TOKEN_SECRET'] =''

user_id = 'ADTARCY'

mkm_sandbox = Mkm(_API_MAP["2.0"]["api"], _API_MAP["2.0"]["api_sandbox_root"])

response = mkm_sandbox.market_place.games()

print(response.json())

