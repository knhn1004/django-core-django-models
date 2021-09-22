from django.db import models


class Product(models.Model):
    """ a single product"""
    title = models.TextField()
    price = models.DecimalField()
