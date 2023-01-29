# Generated by Django 3.0.5 on 2023-01-17 16:27

import bson.objectid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('btc_balance', models.FloatField()),
                ('usd_balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, default=bson.objectid.ObjectId, primary_key=True, serialize=False)),
                ('btc_amount', models.FloatField()),
                ('btc_unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, default=bson.objectid.ObjectId, primary_key=True, serialize=False)),
                ('btc_amount', models.FloatField()),
                ('btc_unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('type', models.CharField(choices=[('buy', 'buy'), ('sell', 'sell')], default='', max_length=4)),
                ('status', models.CharField(choices=[('open', 'open'), ('closed', 'closed')], default='open', max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]