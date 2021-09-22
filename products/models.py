from enum import unique
from django.db import models
from .validators import validate_blocked_words
from core.db.models import BasePublishModel


class Product(BasePublishModel):
    title = models.CharField(max_length=120,
                             validators=[  # this only validate on forms
                                 validate_blocked_words,
                             ],
                             # unique=True
                             )
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    #order = models.IntegerField()

    class Meta:
        ordering = ['-updated', '-timestamp']
        # db_table = '<app_name>_<model_name>' # 'products_product
        # unique_together = [['title', 'order']] # 2 or more fields that need to be unique at the same time
        #verbose_name = 'product'
        #verbose_name_plural = 'products'

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
