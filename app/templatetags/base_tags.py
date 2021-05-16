import re

from django import template

from app.models import Post, InstaUser, Comment

register = template.Library()


@register.simple_tag
def user_like_it(user_id, post):
    if post.likes.filter(id=user_id).exists():
        return True
    else:
        return False


@register.simple_tag
def get_number_of_comments(post):
    return Comment.objects.all().filter(post=post).count()


@register.simple_tag
def get_number_of_posts(user):
    return Post.objects.all().filter(author=user).count()


@register.simple_tag
def get_number_of_followers(user):
    return InstaUser.objects.all().filter(following=user).count()


@register.simple_tag
def user_is_follow(user, follow_user_id):
    if user.following.filter(id=follow_user_id).exists():
        return True
    else:
        return False


@register.simple_tag
def add_hashtags_links(content):
    hashtags = re.findall("[#]\w+", content)
    for hashtag in hashtags:
        content = content.replace(hashtag, f'<a href="/hashtag/{hashtag[1::]}">{hashtag}</a>',1)
    return content
