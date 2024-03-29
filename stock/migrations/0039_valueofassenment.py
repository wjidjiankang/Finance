# Generated by Django 4.1.7 on 2023-03-24 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0038_alter_pegdata_name_alter_stock_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValueOfAssenment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, max_length=20)),
                ('close', models.DecimalField(decimal_places=3, max_digits=10)),
                ('eps_n', models.DecimalField(decimal_places=3, max_digits=10)),
                ('eps_n1', models.DecimalField(decimal_places=3, max_digits=10)),
                ('eps_n2', models.DecimalField(decimal_places=3, max_digits=10)),
                ('voa', models.DecimalField(decimal_places=3, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
