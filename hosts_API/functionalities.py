import requests
import json
from hosts_API.models import *

URL = ...
MOCK = True

def get_all_hosts_data() -> tuple[dict]:
    if MOCK:
        with open('hosts_API/mock_hosts_data.json', 'r') as file:
            data = file.read()
        res = data
    else:
        res = requests.get(URL)
    try:
        if not MOCK:
            res = res.text
        response = json.loads(res)
        hosts = [FullHost(**item) for item in response]
        host = {'message': hosts}, True
        return host
    except Exception as e:
        return {'error': str(e)}, False
