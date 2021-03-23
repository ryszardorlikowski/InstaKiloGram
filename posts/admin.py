from django.contrib import admin
from posts.models import Post, PostLike, PostComment

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)