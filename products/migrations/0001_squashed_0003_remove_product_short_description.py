# Generated by Django 3.2.7 on 2021-09-22 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('products', '0001_initial'), ('products', '0002_auto_20210922_0743'), ('products', '0003_remove_product_short_description')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
    ]
