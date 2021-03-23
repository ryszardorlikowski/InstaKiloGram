from django.urls import path

from posts.views import PostView

urlpatterns = [
    path('view/<int:pk>', PostView.as_view(), name='post'),
]