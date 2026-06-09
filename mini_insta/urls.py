# File: urls.py
# Author: Ignacio Fernandez, ifw@bu.edu
# Description: defines the URL patterns for the mini_insta application

from django.urls import path
from django.contrib.auth import views as auth_views  # built-in login/logout views
from django.views.generic import TemplateView  # simple view for the logout page
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, ShowFeedView, SearchView, ShowMyProfileView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),  # all profiles
    path('profile', ShowMyProfileView.as_view(), name='show_my_profile'),  # logged-in user's own profile
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),  # one profile by pk
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),  # one post by pk
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),  # create a post
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),  # update own profile
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),  # delete a post
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),  # update a post caption
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),  # a profile's followers
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),  # who a profile follows
    path('profile/feed', ShowFeedView.as_view(), name='show_feed'),  # logged-in user's feed
    path('profile/search', SearchView.as_view(), name='search'),  # search profiles and posts
    # authentication
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),  # login page
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),  # log the user out
    path('logout_confirmation/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),  # logout confirmation page
]
