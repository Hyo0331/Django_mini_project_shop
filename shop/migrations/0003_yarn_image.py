# Generated by Django 3.2.10 on 2021-12-16 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20211216_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='yarn',
            name='image',
            field=models.ImageField(blank=True, upload_to='shop/images/%Y/%m/%d/'),
        ),
    ]