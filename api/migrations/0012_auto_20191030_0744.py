# Generated by Django 2.2.6 on 2019-10-30 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20191030_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='total_time',
            field=models.DurationField(default='00:05:00'),
        ),
    ]
