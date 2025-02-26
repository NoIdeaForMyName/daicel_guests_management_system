from .models import *


def get_guardhouse_IPv4() -> str:
    return Setting.objects.all().first().guardhouse_IPv4
