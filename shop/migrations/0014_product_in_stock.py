# Generated by Django 4.1.1 on 2022-12-18 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_remove_attribute_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=0),
        ),
    ]
