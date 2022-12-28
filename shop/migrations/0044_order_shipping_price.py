# Generated by Django 4.1.1 on 2022-12-27 20:21

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0043_alter_order_sale_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[shop.validators.validate_positive]),
        ),
    ]