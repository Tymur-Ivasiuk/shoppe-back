# Generated by Django 4.1.1 on 2022-10-17 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_attributevalues_value_float_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='img/False'),
        ),
    ]
