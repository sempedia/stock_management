# Generated by Django 4.1.7 on 2023-03-14 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_mng', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
    ]
