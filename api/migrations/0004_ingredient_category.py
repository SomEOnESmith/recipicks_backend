# Generated by Django 2.2.6 on 2019-10-29 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191029_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='category',
            field=models.CharField(blank=True, choices=[('Protein', 'Protein'), ('Fruit', 'Fruit'), ('Dairy', 'Dairy'), ('Vegetable', 'Vegetable'), ('Protein', 'Protein'), ('Fruits', 'Fruits')], max_length=20, null=True),
        ),
    ]
