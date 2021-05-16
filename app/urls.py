from django.urls import path
from app.views import Home, SearchUsers, UserPublicProfile, UserEditProfile, PostAdd, PostDetails, PostEdit, \
    PostDelete, CommentDelete, Hashtags, UserFollowingList, UserPosts

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', SearchUsers.as_view(), name='search-users-results'),
    path('profile/<slug>/', UserPublicProfile.as_view(), name='user-public-profile'),
    path('profile/<slug>/posts', UserPosts.as_view(), name='user-posts'),
    path('user/profile/edit/', UserEditProfile.as_view(), name='user-edit-profile'),
    path('post/add/', PostAdd.as_view(), name='post-add'),
    path('post/<int:pk>/', PostDetails.as_view(), name='post-details'),
    path('post/<int:pk>/edit/', PostEdit.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment-delete'),
    path('hashtag/<slug>/', Hashtags.as_view(), name='post-hashtag'),
    path('following/', UserFollowingList.as_view(), name='user-following-list'),

]
