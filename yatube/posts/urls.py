from django.urls import path, include

from . import views

# namespace приложения
app_name = 'posts'

post_patterns = [
    path('<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('<int:post_id>/edit/',
         views.PostEditView.as_view(),
         name='post_edit'),
    path('<int:post_id>/comment/',
         views.AddCommentView.as_view(),
         name='add_comment'),
]

profile_patterns = [
    path('<slug:username>/',
         views.ProfileView.as_view(),
         name='profile'),
    path('<str:username>/follow/',
         views.ProfileFollowView.as_view(),
         name='profile_follow'),
    path('<str:username>/unfollow/',
         views.ProfileUnfollowView.as_view(),
         name='profile_unfollow'),
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', include(post_patterns)),
    path('profile/', include(profile_patterns)),
    path('group/<slug:slug>/', views.GroupPostView.as_view(),
         name='group_list'),
    path('follow/', views.FollowIndexView.as_view(), name='follow_index'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
]