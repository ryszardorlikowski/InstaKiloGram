from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model
from django.template.defaultfilters import slugify
from django.urls import reverse


class InstaUser(AbstractUser):
    full_name = models.CharField(max_length=64, blank=True, null=True)
    about_me = models.TextField(max_length=500, blank=True)
    following = models.ManyToManyField('InstaUser', blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)

        super(InstaUser, self).save(*args, **kwargs)
        avatar = Image.open(self.avatar.path)
        width, height = avatar.size
        if width > 300 or height > 300:
            size = (128, 128)
            avatar.thumbnail(size, Image.ANTIALIAS)
            avatar.save(self.avatar.path)


class Post(Model):
    author = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=400)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(InstaUser, related_name='likes', blank=True)
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.image != None:
            image = Image.open(self.image.path)
            width, height = image.size
            if height > 350 or width > 350:
                height = width / (width / 350)
                width = width / (width / 350)
                size = (width, height)
                image.thumbnail(size, Image.ANTIALIAS)
                image.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post-details', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.id} {self.content[:20]}"


class Comment(Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.content[:20]}"
