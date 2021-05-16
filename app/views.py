from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from app.models import Post, InstaUser, Comment


@method_decorator(login_required, name='dispatch')
class Home(ListView):
    model = Post
    template_name = 'app/home.html'
    paginate_by = 15

    def get_queryset(self):
        posts_list = Post.objects.all().filter(author__in=self.request.user.following.all()).order_by('-created')
        if posts_list.count() == 0:
            messages.success(self.request, 'Nothing to show')
        return posts_list

    def post(self, request, *args, **kwargs):
        if request.GET.get('page'):
            url_query = reverse('home') + f"?page={request.GET.get('page')}"
        else:
            url_query = reverse('home')
        post = Post.objects.get(id=request.POST.get('post_id'))
        manage_likes(request.user, post)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class UserPublicProfile(DetailView):
    model = InstaUser
    template_name = 'app/user_public_profile.html'

    def post(self, request, *args, **kwargs):
        profile_user = InstaUser.objects.get(id=request.POST.get('user_id'))
        message = manage_user_following(request.user, profile_user)
        messages.success(request, message)
        return redirect('user-public-profile', slug=kwargs['slug'])


@method_decorator(login_required, name='dispatch')
class UserEditProfile(UpdateView):
    model = InstaUser
    template_name = 'app/user_edit_profile.html'
    success_url = reverse_lazy('user-edit-profile')
    fields = ['full_name', 'about_me', 'email', 'avatar']

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super(UserEditProfile, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class SearchUsers(ListView):
    model = InstaUser
    template_name = 'app/search_users_results.html'

    def get_queryset(self):
        try:
            query = self.request.GET.get('q')
            if len(query) < 3:
                messages.warning(self.request, "Minimum length of query is 3 characters.")
            else:
                users_list = InstaUser.objects.exclude(username=self.request.user.username).filter(
                    Q(username__contains=query) | Q(full_name__contains=query))
                messages.info(self.request, f"{users_list.count()} results.")
                return users_list
        except (ValueError, TypeError):
            messages.warning(self.request, "Incorrect query.")

    def post(self, request, *args, **kwargs):
        result_user = InstaUser.objects.get(id=request.POST.get('user_id'))
        url_query = reverse("search-users-results") + f"?q={request.GET.get('q')}"
        message = manage_user_following(request.user, result_user)
        messages.success(request, message)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class PostDetails(DetailView):
    model = Post
    template_name = 'app/post_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().filter(post=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('post_id'):
            post = self.get_object()
            manage_likes(request.user, post)

        if request.POST.get('add_comment'):
            if request.POST.get('comment_content'):
                Comment.objects.create(author=request.user, content=request.POST.get('comment_content'),
                                       post=self.get_object())
                messages.success(request, 'Comment has been added')
            else:
                messages.warning(request, "Please fill out comment field")

        return redirect('post-details', pk=self.get_object().id)


@method_decorator(login_required, name='dispatch')
class PostAdd(CreateView):
    model = Post
    template_name = 'app/post_add.html'
    fields = ['content', 'image']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, 'Post has been added')
        return super(PostAdd, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostEdit(UpdateView):
    model = Post
    template_name = 'app/post_edit.html'
    fields = ['content', 'image']

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return redirect("post-details", pk=self.get_object().id)
        else:
            return super(PostEdit, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.edited = True
        self.object.save()
        messages.success(self.request, 'Post has been edited')
        return super(PostEdit, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostDelete(TemplateView):
    template_name = 'app/post_delete.html'

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['pk'])
            if request.user != post.author:
                return redirect('post-details', pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('home')
        return super(PostDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm_delete'):
            Post.objects.get(id=kwargs['pk']).delete()
            messages.success(self.request, 'Post has been deleted')
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class CommentDelete(TemplateView):
    template_name = "app/comment_delete.html"

    def get(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs['pk'])
            post_id = comment.post.id
            if request.user != comment.author:
                return redirect('post-details', post_id)
        except ObjectDoesNotExist:
            return redirect('home')
        return super(CommentDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm_delete'):
            comment = Comment.objects.get(id=kwargs['pk'])
            post_id = comment.post.id
            comment.delete()
            messages.success(self.request, 'Comment has been deleted')
        return redirect('post-details', post_id)


@method_decorator(login_required, name='dispatch')
class Hashtags(ListView):
    model = Post
    template_name = "app/post_hashtags.html"
    slug_field = 'slug'
    paginate_by = 15

    def get_queryset(self):
        return Post.objects.all().filter(Q(content__contains=f"#{self.kwargs['slug']}")).order_by('-created')

    def post(self, request, *args, **kwargs):
        if request.GET.get('page'):
            url_query = reverse('post-hashtag', kwargs={'slug': kwargs['slug']}) + f"?page={request.GET.get('page')}"
        else:
            url_query = reverse('post-hashtag', kwargs={'slug': kwargs['slug']})
        post = Post.objects.get(id=request.POST.get('post_id'))
        manage_likes(request.user, post)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class UserPosts(ListView):
    model = Post
    template_name = "app/user_posts.html"
    slug_field = 'slug'
    paginate_by = 15

    def get_queryset(self):
        return Post.objects.all().filter(author__slug=self.kwargs['slug']).order_by('-created')

    def post(self, request, *args, **kwargs):
        if request.GET.get('page'):
            url_query = reverse('user-posts', kwargs={'slug': kwargs['slug']}) + f"?page={request.GET.get('page')}"
        else:
            url_query = reverse('user-posts', kwargs={'slug': kwargs['slug']})
        post = Post.objects.get(id=request.POST.get('post_id'))
        manage_likes(request.user, post)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class UserFollowingList(ListView):
    model = InstaUser
    template_name = 'app/user_following_list.html'

    def get_queryset(self):
        return self.request.user.following.all()

    def post(self, request, *args, **kwargs):
        user_id = request.POST['user_id']
        followed_user = InstaUser.objects.get(id=user_id)
        message = manage_user_following(request.user, followed_user)
        messages.info(self.request, message)
        return redirect('user-following-list')


def manage_user_following(user, follow_user):
    if user.following.filter(id=follow_user.id).exists():
        user.following.remove(follow_user)
        return f'{follow_user.username} is unfollowed.'
    else:
        user.following.add(follow_user)
        return f'{follow_user.username} is followed.'


def manage_likes(user, post):
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
