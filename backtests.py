import urllib2
import urllib
import json
from os import listdir
from os.path import isfile, join
from collections import namedtuple
import requests
import time
import datetime
import toml
import csv


URL = "http://buckfolio.com:3000/api"
URI_API = URL+"/backtest"
URI_SCANSET = URL+'/scansets'
URI_STRATEGIES = URL+"/strategies"
DIR_STRATEGIES = "../strategies"
DIR_TOML_STRATEGIES = "../config/strategies/"
DATA_SAMPLE = 'configurate_data.json'
TRADE_ADVISOR = 'trading_advisor.json'
TIME_HOUR = 3600
TIME_DAYS = 24*TIME_HOUR
def str_to_date(ts):
    value = datetime.datetime.fromtimestamp(ts)
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")

def scan_set():
    obj = []
    all_scan = requests.post(URI_SCANSET,json={}).json()
    for scanned in all_scan['datasets']:
        obj.append({'coin_inital':scanned['asset'],'date_from':str_to_date(scanned['ranges'][0]['to'] - 7*TIME_DAYS),'date_to':str_to_date(scanned['ranges'][0]['to'])})
    return obj

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
    setScan = scan_set()
    for ss in setScan:
        toml_arr[ss['coin_inital']] = {}
        for json_parsed in all_toml_files:
            toml_dict = dict()
            toml_dict.clear()
            
            data_sample = json.loads(open(DATA_SAMPLE,'r').read())
            data_sample['watch']['asset'] = ss['coin_inital']
            data_sample['backtest']['daterange']['from'] = ss['date_from']
            data_sample['backtest']['daterange']['to'] = ss['date_to']

            data_advisor = json.loads(open(TRADE_ADVISOR,'r').read())
            data_advisor['tradingAdvisor']['method'] = json_parsed
            
            toml_dict.update(data_sample)
            toml_dict.update(data_advisor)
            toml_dict.update({json_parsed:all_toml_files[json_parsed]})
            
            toml_arr[ss['coin_inital']][json_parsed] = toml_dict

    return toml_arr

def do_request():
    n = create_post_request()
    csvfile = open('backtests.csv', 'w')
    fieldnames = ["COIN_NAME","STRATEGY","START DATE","FINISH DATE","START BALANCE","END BALANCE","% WIN","TRADES NUM"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for a in n:
        for y in n[a]:
            try:
                q = requests.post(URI_API,json=n[a][y]).json()
                if 'performanceReport' in q:
                    row = {
                        "COIN_NAME":n[a][y]['watch']['asset'],
                        "STRATEGY": y,
                        "START DATE":q['performanceReport']['startTime'],
                        "FINISH DATE":q['performanceReport']['endTime'],
                        "START BALANCE":str(q['performanceReport']['startBalance']),
                        "END BALANCE":str(q['performanceReport']['balance']),
                        "% WIN":str(q['performanceReport']['relativeProfit']),
                        "TRADES NUM":q['performanceReport']['trades']
                    }
                    writer.writerow(row)
            except ValueError:
                print(ValueError.message)

do_request()
