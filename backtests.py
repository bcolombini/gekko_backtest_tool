import urllib2
import urllib
import json
from os import listdir
from os.path import isfile, join
from collections import namedtuple
import requests
import toml

URL = "http://buckfolio.com:3000/api"
URI_API = URL+"/backtest"
URI_STRATEGIES = URL+"/strategies"
DIR_STRATEGIES = "../strategies"
DIR_TOML_STRATEGIES = "../config/strategies/"
DATA_SAMPLE = 'configurate_data.json'
TRADE_ADVISOR = 'trading_advisor.json'

def strategies_from_api():
    toml_dict = dict()
    strategies = requests.get(URI_STRATEGIES).json()
    for strategy in strategies:
        toml_dict.update({strategy['name']:toml.loads(strategy['params'])})
    return toml_dict

def strategies_names():
    return [f.replace(".js","") for f in listdir(DIR_STRATEGIES) if isfile(join(DIR_STRATEGIES, f)) and ".js" in f]

def create_post_request():
    
    toml_arr = {}
    data_sample = json.loads(open(DATA_SAMPLE,'r').read())
    all_toml_files = strategies_from_api()

    for json_parsed in all_toml_files:
        toml_dict = dict()
        toml_dict.clear()
        data_advisor = json.loads(open(TRADE_ADVISOR,'r').read())
        data_advisor['tradingAdvisor']['method'] = json_parsed
        toml_dict.update(data_sample)
        toml_dict.update(data_advisor)
        toml_dict.update({json_parsed:all_toml_files[json_parsed]})
        
        toml_arr[json_parsed] = toml_dict        
    return toml_arr

def do_request():
    n = create_post_request()
    print("STRATEGY --- START DATE --- FINISH DATE --- START AMOUNT --- END AMOUNT --- % WIN --- TRADES NUM ")
    for a in n:
        try:
            q = requests.post(URI_API,json=n[a]).json()
            if 'performanceReport' in q:
                print(a+" --- "+str(q['performanceReport']['startTime'])+" --- "+str(q['performanceReport']['endTime'])+" --- "+str(q['performanceReport']['startBalance'])+" --- "+str(q['performanceReport']['balance'])+" --- "+str(q['performanceReport']['relativeProfit'])+"% --- "+str(q['performanceReport']['trades']))
        except ValueError:
            print(a+" --- ")

do_request()
