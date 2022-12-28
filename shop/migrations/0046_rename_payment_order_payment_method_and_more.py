# Generated by Django 4.1.1 on 2022-12-28 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0045_remove_order_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment',
            new_name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]