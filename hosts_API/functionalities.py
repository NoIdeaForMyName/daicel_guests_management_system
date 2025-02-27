import requests
import json
from hosts_API.models import *

URL = ...
MOCK = True

def get_all_hosts_data() -> tuple[dict, bool]:
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

def get_all_hosts_data_dict() -> tuple[dict, bool]:
    hosts, success = get_all_hosts_data()
    if not success:
        return hosts, success
    hosts_dict = [host.to_dict() for host in hosts['message']]
    return {'message': hosts_dict}, True


def authenticate_user(username=None, password=None):
    if not (username or password):
        return False
    if MOCK:
        from random import random, randint
        if random() > 0.5:
            return randint(3, 5)
        return -1
