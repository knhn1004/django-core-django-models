from django.db import models
from .validators import validate_blocked_words


class Product(models.Model):
    """ a single product"""
    title = models.CharField(max_length=120,
                             validators=[
                                 validate_blocked_words,
                             ])  # this only validate on forms
    description = models.TextField(null=True)
    #short_description = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        # to validate on any creation
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)
