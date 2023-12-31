# Generated by Django 4.2.2 on 2023-06-08 23:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_products_last_time_sold_sells'),
    ]

    operations = [
        migrations.AddField(
            model_name='sells',
            name='product_name',
            field=models.CharField(default='hellyea', max_length=225),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Adds',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('product_name', models.CharField(max_length=225)),
                ('quantity', models.PositiveIntegerField()),
                ('date_added', models.DateTimeField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.products')),
            ],
        ),
    ]
