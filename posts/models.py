from django.db import models
from django.urls import reverse_lazy

from accounts.models import User


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, verbose_name='Użytkownik')
    image = models.ImageField(upload_to='posts', verbose_name='Obrazek')
    description = models.CharField(max_length=200, verbose_name='Opis')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Dodano')

    @property
    def likes_count(self):
        return PostLike.objects.filter(post=self).count()

    @property
    def comments_count(self):
        return PostComment.objects.filter(post=self).count()

    def get_absolute_url(self):
        return reverse_lazy('posts:post', kwargs={'pk': self.pk})

    class Meta:
        verbose_name='Post'
        verbose_name_plural='Posty'

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Użytkownik')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')

    class Meta:
        verbose_name='Polubienie'
        verbose_name_plural='Polubienia'

class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Użytkownik')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    content = models.TextField(verbose_name='Treść')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Dodano')

    class Meta:
        verbose_name='Komentarz'
        verbose_name_plural='Komentarze'