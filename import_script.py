import requests
import json

URL = "http://buckfolio.com:3000/api/"
URI_IMPORT = URL+"import"
object_to_import = json.loads(open('import.json','r').read())
par_value = [
"GRC",
"HUC",
"LTC",
"MAID",
"OMNI",
"NAV",
"NEOS",
# "NMC",
# "NXT",
# "POT",
# "PPC",
# "STR",
# "SYS",
# "VIA",
# "VRC",
# "VTC",
# "XBC",
# "XCP",
# "XEM",
# "XMR",
# "XPM",
# "XRP",
# "ETH",
# "SC",
# "EXP",
# "FCT",
# "AMP",
# "DCR",
# "LSK",
# "LBC",
# "STEEM",
# "SBD",
# "ETC",
# "REP",
# "ARDR",
# "ZEC",
# "STRAT",
# "PASC",
# "GNT",
# "GNO",
# "BCH",
# "ZRX",
# "CVC",
# "OMG",
# "GAS",
# "STORJ",
# "EOS",
# "SNT",
# "KNC",
# "BAT",
# "LOOM"
]

for x in par_value:
    object_to_import['watch']['asset'] = x
    print(requests.post(URI_IMPORT,json=object_to_import).json())
