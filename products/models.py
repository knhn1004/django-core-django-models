from django.conf import settings
from django.db import models
from .validators import validate_blocked_words
from core.db.models import BasePublishModel
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save

User = settings.AUTH_USER_MODEL # "auth.User"


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

    # slug
    slug = models.SlugField(blank=True, null=True, db_index=True)

    #order = models.IntegerField()

    tags = models.TextField(null=True)

    # user FK
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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

    def get_absolute_url(self):
        # '/products/my-awesome-product/'
        # '/products/1/'
        return f"/product/{self.slug}/"


def slugify_pre_save(sender, instance, *args, **kwargs):
    # create my slug from my title
    if instance.slug is None or instance.slug == "":
        new_slug = slugify(instance.title)
        Klass = instance.__class__
        #qs = Product.objects.filter(slug=new_slug)
        #qs = Klass.objects.filter(slug=new_slug)
        qs = Klass.objects.filter(slug=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.slug = new_slug
        else:
            instance.slug = f"{new_slug}-{qs.count()}"


pre_save.connect(slugify_pre_save, sender=Product)
