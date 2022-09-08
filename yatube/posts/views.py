from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import DataMixin


class IndexView(DataMixin, ListView):
    """Главная страница написанная на CBV."""
    model = Post
    template_name = 'posts/index.html'
    # context_object_name не обязательно указывать. paginate_by создает объект
    # page_obj, из которого берется контекст для страницы

    def get_queryset(self):
        return Post.objects.select_related('group', 'author')


class GroupPostView(DataMixin, DetailView, MultipleObjectMixin):
    """Отображение постов по группам"""
    model = Group
    allow_empty = False
    template_name = 'posts/group_list.html'

    def get_context_data(self, **kwargs):
        object_list = (Post.objects
                       .filter(group=self.get_object())
                       .select_related('author'))
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class ProfileView(DataMixin, ListView):
    """Профиль пользователя"""
    model = Post
    slug_url_kwarg = 'username'
    template_name = 'posts/profile.html'

    def get_queryset(self):
        return (
            Post.objects
            .filter(author__username=self.kwargs['username'])
            .select_related('group', 'author')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = get_object_or_404(User, username=self.kwargs['username'])
        context['author'] = username
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                user=self.request.user, author=username
            ).select_related('author', 'user')
        return context


class PostDetailView(DetailView):
    """Подробное описание поста"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context['form'] = CommentForm()
        context['comments'] = post.comments.select_related('author')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Добавление поста"""
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        return redirect('posts:profile', self.request.user)


class PostEditView(LoginRequiredMixin, UpdateView):
    """Редактирование поста"""
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def get_object(self, queryset=None):
        """Получить редактируемый объект"""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def dispatch(self, request, *args, **kwargs):
        """Проверка на то, что только автор может редактировать"""
        post = self.get_object()
        if not post.author == self.request.user:
            return HttpResponse(status=HTTPStatus.FOUND)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse('posts:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class AddCommentView(LoginRequiredMixin, CreateView):
    """Добавление комментария к посту"""
    form_class = CommentForm
    template_name = 'posts/post_detail.html'
    slug_url_kwarg = 'post_id'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post_id = self.kwargs['post_id']
        comment.save()
        return redirect('posts:post_detail', post_id=self.kwargs['post_id'])


class FollowIndexView(DataMixin, LoginRequiredMixin, ListView):
    """Просмотр постов избранных авторов"""
    model = Post
    template_name = 'posts/follow.html'

    def get_queryset(self):
        return Post.objects.filter(
            author__in=self.request.user.follower.all().values('author')
        ).select_related('group', 'author')


class ProfileFollowView(LoginRequiredMixin, View):
    """Подписка на автора"""

    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        if request.user.username == username:
            messages.error(request, 'Вы не можете подписываться сам на себя')
            return HttpResponseBadRequest()
        Follow.objects.get_or_create(user=request.user, author=author)
        messages.success(request, f'Вы успешно подписались на {author}')
        return redirect('posts:profile', username=author)


class ProfileUnfollowView(LoginRequiredMixin, View):
    """Отписка от автора"""

    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        Follow.objects.filter(user=request.user, author=author).delete()
        messages.error(request, f'Вы отписались от {author}')
        return redirect('posts:profile', username=author)
