# Generated by Django 5.1.6 on 2025-02-26 16:50

from django.db import migrations


def initial_settings(apps, schema_editor):
    Setting = apps.get_model("system_settings", "Setting")
    settings = Setting.objects.all()
    setting = settings[0] if len(settings) > 0 else Setting(guardhouse_IPv4="127.0.0.1")
    for i in range(1, len(settings)):
        settings[i].delete()
    setting.save()

class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_settings),
    ]
