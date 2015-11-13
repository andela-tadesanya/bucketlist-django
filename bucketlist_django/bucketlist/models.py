from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bucketlist(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField()
    date_modified = models.DateField()
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

