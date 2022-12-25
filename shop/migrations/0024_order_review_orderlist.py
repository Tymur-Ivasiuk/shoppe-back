# Generated by Django 4.1.1 on 2022-12-25 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0023_remove_orderlist_order_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('New', 'New'), ('In processing', 'In processing'), ('Confirmed', 'Confirmed'), ('Delivered', 'Delivered'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='New', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[shop.validators.validate_positive])),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('postcode', models.PositiveSmallIntegerField()),
                ('town', models.CharField(max_length=255)),
                ('phone', phone_field.models.PhoneField(max_length=31)),
                ('email', models.EmailField(max_length=254)),
                ('order_notes', models.TextField(blank=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('star_rating', models.PositiveSmallIntegerField(default=1, validators=[shop.validators.starValid])),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
            ],
        ),
    ]