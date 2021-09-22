from django.db import models
from .validators import validate_blocked_words
from core.db.models import BasePublishModel


class Product(BasePublishModel):
    title = models.CharField(max_length=120,
                             validators=[
                                 validate_blocked_words,
                             ])  # this only validate on forms
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
