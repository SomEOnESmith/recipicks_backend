# Generated by Django 2.2.6 on 2019-11-03 11:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191031_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='total_time',
            field=models.DurationField(default=datetime.datetime(2019, 11, 3, 11, 37, 57, 386706, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='step',
            name='required_time',
            field=models.DurationField(),
        ),
    ]
