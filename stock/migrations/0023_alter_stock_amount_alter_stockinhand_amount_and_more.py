# Generated by Django 4.1.2 on 2022-11-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0022_alter_stockinhand_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='stockinhand',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
        migrations.AlterField(
            model_name='stockinhand',
            name='cost',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockinhand',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='stockinhand',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
