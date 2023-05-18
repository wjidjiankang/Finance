# Generated by Django 4.1.7 on 2023-04-11 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0046_stockinhand_value_proportion'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='sell_profit',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockinhand',
            name='value_proportion',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]