import asyncio
from pyosu import OsuApi

import json

with open( 'config.json') as config_file:
    temp = json.load( config_file )

apikey = temp['osuapikey']

osu = OsuApi(apikey)
