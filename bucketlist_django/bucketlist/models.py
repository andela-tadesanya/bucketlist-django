from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bucketlist(models.Model):
    name = models.CharField(
                            'bucketlist name',
                             max_length=50,
                             blank=False)
    date_created = models.DateTimeField('created on',
                                         auto_now_add=True)
    date_modified = models.DateTimeField('date last modified'
                                         auto_now=True)
    created_by = models.ForeignKey(User)

    class Meta:
        ordering = ['date_created']
        verbose_name = 'bucketlist'
        verbose_name_plural = 'bucketlists'

    def __unicode__(self):
        return self.name

class BucketlistItem(models.Model):
    name = models.CharField('bucketlist item name', max_length=150, blank=False)
    date_created = models.DateTimeField('created on',
                                         auto_now_add=False)
    date_modified = models.DateTimeField('last modified'
                                         auto_now=False)
    done = models.BooleanField('Done',
                                default=False)
    bucketlist = models.ForeignKey(Bucketlist)

    class Meta:
        ordering = [date_created]
        verbose_name = 'bucketlist item'
        verbose_name_plural = 'bucketlist items'

    def __unicode__(self):
        return self.name