from django.contrib.auth.backends import BaseBackend
from hosts_API.functionalities import authenticate_user
from django.contrib.auth.models import User


class SymfoniaBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # here API call to check if given credentials are OK
        # if so -> authenticate user
        # else -> return None
        user_id = authenticate_user(username, password)
        if user_id == -1:
            return None
        else:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = User(id=user_id, username=username)
                user.save()
            return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        return user
