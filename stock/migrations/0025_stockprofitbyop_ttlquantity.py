# Generated by Django 4.1.2 on 2022-11-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0024_stockprofitbyop'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockprofitbyop',
            name='ttlquantity',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=8),
        ),
    ]
