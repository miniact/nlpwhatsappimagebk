# Generated by Django 3.2 on 2021-05-07 07:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ads_pubtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='pubtime',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 7, 7, 22, 9, 349388, tzinfo=utc)),
        ),
    ]