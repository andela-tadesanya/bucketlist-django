from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here
class Bucketlist(models.Model):
    name = models.CharField('bucketlist name',
                            max_length=50,
                            blank=False)
    date_created = models.DateTimeField('created on',
                                        null=True,
                                        blank=True,
                                        auto_now_add=True)
    date_modified = models.DateTimeField('date last modified',
                                         null=True,
                                         blank=True,
                                         auto_now=True)
    created_by = models.ForeignKey(User, related_name='bucketlists')

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'bucketlist'
        verbose_name_plural = 'bucketlists'

    def __unicode__(self):
        return self.name


class BucketlistItem(models.Model):
    name = models.CharField('bucketlist item name',
                            max_length=150,
                            blank=False)
    date_created = models.DateTimeField('created on',
                                        null=True,
                                        blank=True,
                                        auto_now_add=True)
    date_modified = models.DateTimeField('last modified',
                                         null=True,
                                         blank=True,
                                         auto_now=True)
    done = models.BooleanField('Done',
                               default=False)
    bucketlist = models.ForeignKey(Bucketlist, related_name='bucketlistitems')

    class Meta:
        ordering = ['date_created']
        verbose_name = 'bucketlist item'
        verbose_name_plural = 'bucketlist items'

    def __unicode__(self):
        return self.name


# automatically generate tokens for newly created users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
