from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='images', default='images/default.png', blank=True, null=True)
    about_me = models.ImageField(max_length=500, blank=True, null=True)
    following = models.ManyToManyField('User', related_name='followers' )