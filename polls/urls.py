from django.conf.urls.static import static
from django.urls import path

from sitesurvey import settings
from .views import index, login_view, register, logout_view, profile, edit_profile, delete_profile, \
    post_detail, edit_post, delete_post, create_post, add_comment, edit_comment, delete_comment, like_post

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('posts/create_post/', create_post, name='create_post'),
    path('posts/<slug:post_slug>/', post_detail, name='post_detail'),
    path('posts/edit/<slug:post_slug>/', edit_post, name='edit_post'),
    path('posts/delete/<slug:post_slug>/', delete_post, name='delete_post'),
    path('post/<slug:post_slug>/comment/add/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('post/<slug:post_slug>/like/', like_post, name='like_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
