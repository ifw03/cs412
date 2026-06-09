# File: admin.py
# Author: Ignacio Fernandez, ifw@bu.edu
# Description: registers the mini_insta models with the django admin site
from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow, Comment, Like

admin.site.register(Profile)  # manage profiles in admin
admin.site.register(Post)  # manage posts in admin
admin.site.register(Photo)  # manage photos in admin
admin.site.register(Follow)  # manage follow relationships in admin
admin.site.register(Comment)  # manage comments in admin
admin.site.register(Like)  # manage likes in admin
