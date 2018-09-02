import requests
import json

URL = "http://buckfolio.com:3000/api/"
URI_IMPORT = URL+"import"
object_to_import = json.loads(open('import.json','r').read())
par_value = [
"LTC",
"SYS",
"XMR",
"ETH",
"DCR",
"ETC",
"BCH",
]
for x in par_value:
    object_to_import['watch']['asset'] = x
    print(requests.post(URI_IMPORT,json=object_to_import).json())
