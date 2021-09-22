from django.db import models


class Product(models.Model):
    """ a single product"""
    title = models.CharField(max_length=120)
    description = models.TextField(null=True)
    #short_description = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=20, decimal_places=2)
