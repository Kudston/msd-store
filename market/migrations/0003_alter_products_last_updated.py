# Generated by Django 4.2.1 on 2023-06-06 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_alter_products_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
