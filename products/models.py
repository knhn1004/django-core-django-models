from django.db import models
from .validators import validate_blocked_words
from core.db.models import BasePublishModel
from django.utils import timezone


class ProductQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=Product.PublishStateOptions.PUBLISH,
                           publish_timestamp__lte=now)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def published(self):
        # Product.objects.filter()
        now = timezone.now()
        # return self.get_queryset().filter(state=Product.PublishStateOptions.PUBLISH,
        #                                  publish_timestamp__lte=now)
        # Product.objects.published()
        # Product.objects.filter(title__icontains='Title').published()
        return self.get_queryset().published()


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

    ''' cutom manager '''
    objects = ProductManager()

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
