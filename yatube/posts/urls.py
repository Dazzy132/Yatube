from django.urls import path
from . import views

# namespace
app_name = 'posts'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('group/<slug:slug>/', views.group_posts, name='group_list'),
    # path('profile/<str:username>/', views.profile, name='profile'),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # path('posts/<int:post_id>/comment/',
    #      views.add_comment, name='add_comment'),
    # path('create/', views.post_create, name='post_create'),


    path('', views.IndexView.as_view(), name='index'),
    # django.views.decorators.cache import cache_page
    # path('', cache_page(5)(views.IndexView.as_view()), name='index'),
    path('group/<slug:slug>/',
         views.GroupPostView.as_view(), name='group_list'),
    path('profile/<slug:username>/',
         views.ProfileView.as_view(), name='profile'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/edit/',
         views.PostEditView.as_view(), name='post_edit'),
    path('posts/<int:post_id>/comment/',
         views.AddCommentView.as_view(), name='add_comment'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),

    path('follow/', views.FollowIndexView.as_view(), name='follow_index'),

    path('profile/<str:username>/follow/',
         views.ProfileFollowView.as_view(), name='profile_follow'
         ),

    path('profile/<str:username>/unfollow/',
         views.ProfileUnfollowView.as_view(), name='profile_unfollow'
         ),
]
