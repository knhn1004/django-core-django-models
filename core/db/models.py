from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError


class BasePublishModel(models.Model):
    class Meta:
        abstract = True

    class PublishStateOptions(models.TextChoices):
        PUBLISH = 'PU', 'Published',
        DRAFT = 'DR', 'Draft'
        PRIVATE = 'PR', 'Private'

    state = models.CharField(max_length=120,
                             default=PublishStateOptions.DRAFT,
                             choices=PublishStateOptions.choices
                             )

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
        return self.state == self.PublishStateOptions.PUBLISH

    @property
    def is_published(self):
        publish_timestamp = self.publish_timestamp
        return self.state_is_published and publish_timestamp <= timezone.now()

    def save(self, *args, **kwargs):
        ''' setup publish timestamp '''
        if self.state_is_published and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        else:
            self.publish_timestamp = None
        super().save(*args, **kwargs)
