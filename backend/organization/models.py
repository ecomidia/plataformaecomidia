from django.db import models

# Create your models here.

class Organization(models.Model):
    organization = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    facebook_url = models.URLField(null=True)
    instagram_url = models.URLField(null=True)
    twitter_url = models.URLField(null=True)
