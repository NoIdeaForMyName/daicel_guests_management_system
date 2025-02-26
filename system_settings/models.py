from django.db import models

class Setting(models.Model):
    guardhouse_IPv4 = models.CharField(max_length=15)
    def __str__(self):
        return f'guardhouse_IPv4: {self.guardhouse_IPv4}'
