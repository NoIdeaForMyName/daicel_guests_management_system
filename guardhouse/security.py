from ipware import get_client_ip
from django.http import HttpResponseForbidden
import system_settings.functionalities as settings
from functools import wraps


def validate_ip(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        ip, _ = get_client_ip(request)
        if ip != settings.get_guardhouse_IPv4():
            return HttpResponseForbidden(f'Invalid IPv4 address: {ip}')
        return func(request, *args, **kwargs)
    return wrapper
