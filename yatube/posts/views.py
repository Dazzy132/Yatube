# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# from django.views.decorators.cache import cache_page
from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import DataMixin, paginate_queryset

# def index(request):
#     """Главная страница"""
#     post_list = (
#         Post.objects
#         .select_related('group', 'author')
#     )
#     page_obj = paginate_queryset(request, post_list)
#     context = {
#         'page_obj': page_obj
#     }
#     return render(request, 'posts/index.html', context)


class IndexView(DataMixin, ListView):
    """Главная страница написанная на CBV."""
    model = Post
    template_name = 'posts/index.html'
    # context_object_name не обязательно указывать. paginate_by создает объект
    # page_obj, из которого берется контекст для страницы

    def get_queryset(self):
        return Post.objects.select_related('group', 'author').distinct()


def group_posts(request, slug):
    """Отображение постов по группам"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author')
    page_obj = paginate_queryset(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


class GroupPostView(DataMixin, ListView):
    """Отображение постов по группам"""
    model = Post
    allow_empty = False
    template_name = 'posts/group_list.html'

    def get_queryset(self):
        return Post.objects.filter(group__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(slug=self.kwargs['slug'])
        return context


# def profile(request, username):
#     """Профиль пользователя"""
#     user = get_object_or_404(User, username=username)
#     user_posts = user.posts.select_related('group')
#     count_posts = user_posts.count()
#     page_obj = paginate_queryset(request, user_posts)
#     context = {
#         'page_obj': page_obj,
#         'count_posts': count_posts,
#         'username': user
#     }
#     return render(request, 'posts/profile.html', context)


class ProfileView(DataMixin, ListView):
    """Профиль пользователя"""
    model = Post
    slug_url_kwarg = 'username'
    template_name = 'posts/profile.html'

    def get_queryset(self):
        return (
            Post.objects
            .filter(author__username=self.kwargs['username'])
            .select_related('group')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = get_object_or_404(User, username=self.kwargs['username'])
        # context['username'] = (
        #     username if username.get_full_name()
        #     else self.kwargs['username']
        # )
        context['author'] = username
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                user=self.request.user, author=username
            )
        return context


# def post_detail(request, post_id):
#     """Подробное описание поста"""
#     post = get_object_or_404(Post, pk=post_id)
#     count_posts = post.author.posts.count()
#     context = {
#         'post': post,
#         'count_posts': count_posts,
#         'comments': post.comments.all(),
#         'form': CommentForm()
#     }
#     return render(request, 'posts/post_detail.html', context)


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
        context['comments'] = post.comments.all()
        return context


# @login_required
# def post_create(request):
#     """Добавление поста"""
#     form = PostForm(request.POST or None, files=request.FILES or None)
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.save()
#         return redirect('posts:profile', request.user)
#     return render(request, 'posts/create_post.html', {'form': form})


class PostCreateView(LoginRequiredMixin, CreateView):
    """Добавление поста"""
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        return redirect('posts:profile', self.request.user)


# @login_required
# def post_edit(request, post_id):
#     """Редактирование поста"""
#     post = get_object_or_404(Post, pk=post_id)
#     # Благодаря instance и экземпляру модели - возможно редактирование
#     if request.user == post.author:
#         form = PostForm(
#             request.POST or None,
#             files=request.FILES or None,
#             instance=post
#         )
#         if form.is_valid():
#             # post = form.save(commit=False)
#             # post.author = request.user
#             post.save()
#             return redirect('posts:post_detail', post.pk)
#         form = PostForm(instance=post)
#         return render(request, 'posts/create_post.html', {'form': form,
#                                                           'post': post,
#                                                           'is_edit': True})
#     # return redirect('posts:post_detail', post_id)
#     return HttpResponse(status=403)


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
            return HttpResponse(status=302)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_success_url(self):
        # return redirect('posts:post_detail', self.kwargs['post_id'])
        return '{}'.format(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.kwargs['post_id']}))


# @login_required
# def add_comment(request, post_id):
#     """Добавление комментария к посту"""
#     post = get_object_or_404(Post, pk=post_id)
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user
#         comment.post_id = post_id
#         comment.save()
#         return redirect('posts:post_detail', post_id=post.pk)
#     return render(request, 'posts/post_detail.html')


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
        # for x in self.request.user.follower.all():
        #     print(x.author.get_username)
        return Post.objects.filter(
            author__in=self.request.user.follower.all().values('author')
        )


class ProfileFollowView(LoginRequiredMixin, View):
    """Подписка на автора"""

    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        # Какую лучше применить ошибку, если пользователь пытается делать
        # такие действия? Знаю только редирект
        if request.user.username == username:
            return redirect('posts:profile', username=author)
        if Follow.objects.filter(
                user=request.user, author=author).exists():
            return redirect('posts:profile', username=author)
        Follow.objects.create(user=request.user, author=author).save()
        messages.success(request, f'Вы успешно подписались на {author}')
        return redirect('posts:profile', username=author)


class ProfileUnfollowView(LoginRequiredMixin, View):
    """Отписка от автора"""

    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        Follow.objects.filter(user=request.user, author=author).delete()
        messages.error(request, f'Вы отписались от {author}')
        return redirect('posts:profile', username=author)