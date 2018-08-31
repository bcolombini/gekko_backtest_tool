import urllib2
import urllib
import json
from os import listdir
from os.path import isfile, join
from collections import namedtuple
import requests
import toml

URL_API = "http://buckfolio.com:3000/api/backtest"
DIR_STRATEGIES = "../strategies"
DIR_TOML_STRATEGIES = "../config/strategies/"
DATA_SAMPLE = '{"watch":{"exchange":"poloniex","currency":"BTC","asset":"ETH"},"paperTrader":{"feeMaker":0.25,"feeTaker":0.25,"feeUsing":"maker","slippage":0.05,"simulationBalance":{"asset":0.2,"currency":100},"reportRoundtrips":true,"enabled":true},"backtest":{"daterange":{"from":"2018-05-30T22:43:00Z","to":"2018-08-31T00:36:00Z"}},"backtestResultExporter":{"enabled":true,"writeToDisk":false,"data":{"stratUpdates":false,"roundtrips":true,"stratCandles":true,"stratCandleProps":["open"],"trades":true}},"performanceAnalyzer":{"riskFreeReturn":2,"enabled":true},"valid":true}'
TRADE_ADVISOR = '{"tradingAdvisor": {"enabled": true,"method": "RSI","candleSize": 15,"historySize": 1}}'


def strategies_names():
    return [f.replace(".js","") for f in listdir(DIR_STRATEGIES) if isfile(join(DIR_STRATEGIES, f)) and ".js" in f]

def parse_toml_file():
    toml_dict = dict()
    for strategy_name in strategies_names(): 
        if isfile(DIR_TOML_STRATEGIES+strategy_name+'.toml'):
            result = toml.loads(open(DIR_TOML_STRATEGIES+strategy_name+'.toml','r').read())
            toml_dict.update({strategy_name:result})
    return toml_dict

def create_post_request():
    
    toml_arr = {}
    data_advisor = json.loads(TRADE_ADVISOR)
    data_sample = json.loads(DATA_SAMPLE)
    all_toml_files = parse_toml_file()

    for json_parsed in all_toml_files:
        toml_dict = dict()
        toml_dict.clear()
        data_advisor = json.loads(TRADE_ADVISOR)
        data_advisor['tradingAdvisor']['method'] = json_parsed
        toml_dict.update(data_sample)
        toml_dict.update(data_advisor)
        toml_dict.update({json_parsed:all_toml_files[json_parsed]})
        
        toml_arr[json_parsed] = toml_dict        
    return toml_arr

def do_request():
    n = create_post_request()
    for a in n:
        try:
            q = requests.post(URL_API,json=n[a]).json()
            if 'performanceReport' in q:
                print(a+" - "+str(q['performanceReport']['relativeProfit']))
        except ValueError:
            print(ValueError.message)

do_request()
