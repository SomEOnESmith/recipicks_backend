# Generated by Django 2.2.6 on 2019-11-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(choices=[('Protein', 'Protein'), ('Vegetable', 'Vegetable'), ('Fruit', 'Fruit'), ('Dairy', 'Dairy'), ('Grain', 'Grain'), ('Bean', 'Bean'), ('Nut', 'Nut'), ('Others', 'Others')], default='Others', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='step',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
