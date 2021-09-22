#import datetime
from django.utils import timezone
from django.db import models
from .validators import validate_blocked_words
from django.core.exceptions import ValidationError


class Product(models.Model):
    class ProductStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Published',
        DRAFT = 'DR', 'Draft'
        PRIVATE = 'PR', 'Private'

    title = models.CharField(max_length=120,
                             validators=[
                                 validate_blocked_words,
                             ])  # this only validate on forms
    state = models.CharField(max_length=120,
                             default=ProductStateOptions.DRAFT,
                             choices=ProductStateOptions.choices
                             )
    description = models.TextField(null=True)
    #short_description = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    # auto set when this object was created
    timestamp = models.DateTimeField(auto_now_add=True,
                                     # default=datetime.datetime.now,
                                     # default=timezone.now
                                     )

    # auto set when this object was last saved
    updated = models.DateTimeField(auto_now=True)

    # auto set when the state is changed to `PUBLISH`
    publish_timestamp = models.DateTimeField(auto_now_add=False,
                                             auto_now=False,
                                             null=True
                                             )

    @property
    def state_is_published(self):
        return self.state == self.ProductStateOptions.PUBLISH

    @property
    def is_published(self):
        publish_timestamp = self.publish_timestamp
        return self.state_is_published and publish_timestamp <= timezone.now()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # to validate on any creation
        validate_blocked_words(self.title)

        ''' setup publish timestamp '''
        if self.state_is_published and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        else:
            self.publish_timestamp = None
        super().save(*args, **kwargs)

    """
    def clean(self):
        '''
        Django Model Forms / Django Forms
        Project.objects.create() -> not call .clean()
        '''
        if self.title == self.description:
            raise ValidationError('Make the description different')

    """
