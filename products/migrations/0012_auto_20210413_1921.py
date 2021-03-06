# Generated by Django 3.1.7 on 2021-04-13 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_orderedproducts_orders'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderedproducts',
            options={'verbose_name_plural': 'Ordered products'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name_plural': 'Orders'},
        ),
        migrations.AddField(
            model_name='orderedproducts',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
