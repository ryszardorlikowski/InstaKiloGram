from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='images', default='images/default.png', blank=True, null=True,
                                      verbose_name='Zdjęcie')
    about_me = models.TextField(max_length=500, blank=True, null=True, verbose_name='O mnie')
    following = models.ManyToManyField('User', related_name='followers',blank=True, null=True, verbose_name="Obserwowani")

    def get_absolute_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.pk})