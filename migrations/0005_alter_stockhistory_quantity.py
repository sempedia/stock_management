# Generated by Django 4.1.7 on 2023-03-15 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_mng', '0004_remove_stock_date_stockhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='quantity',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
