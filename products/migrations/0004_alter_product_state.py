# Generated by Django 3.2.7 on 2021-09-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='state',
            field=models.CharField(choices=[('draft', 'DRAFT'), ('publish', 'PUBLISH'), ('private', 'PRIVATE')], default='draft', max_length=120),
        ),
    ]