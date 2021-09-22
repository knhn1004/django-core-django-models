from django.db import models
from .validators import validate_blocked_words
from django.core.exceptions import ValidationError


# (DB_VALUE, USER_FACING_VALUE)
PUBLISH_STATE_CHOICES = [
    ('draft', 'DRAFT'),
    ('publish', 'PUBLISH'),
    ('private', 'PRIVATE')
]


class Product(models.Model):
    """ a single product"""
    title = models.CharField(max_length=120,
                             validators=[
                                 validate_blocked_words,
                             ])  # this only validate on forms
    state = models.CharField(max_length=120,
                             default='DRAFT',
                             choices=PUBLISH_STATE_CHOICES,
                             )
    description = models.TextField(null=True)
    #short_description = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        # to validate on any creation
        validate_blocked_words(self.title)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.state == 'PUBLISH'

    def __str__(self):
        return self.title

    """
    def clean(self):
        '''
        Django Model Forms / Django Forms
        Project.objects.create() -> not call .clean()
        '''
        if self.title == self.description:
            raise ValidationError('Make the description different')

    """
