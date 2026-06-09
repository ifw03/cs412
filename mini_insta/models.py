# File: models.py
# Author: Ignacio Fernandez, ifw@bu.edu
# Description: defines the data models for the mini_insta application

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  # built-in user model for authentication

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a instagram profile '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # the user this profile belongs to
    username = models.TextField(blank=False)  # handle shown on the profile
    display_name = models.TextField(blank=False)  # full name shown on the profile
    profile_image_url = models.URLField(blank=True)  # link to the avatar image
    bio_text = models.TextField(blank=False)  # short bio blurb
    join_date = models.DateTimeField(auto_now=True)  # when the profile was created

    def __str__(self):
        '''Return a string representation of this profile'''
        return f'{self.username} ({self.display_name})'

    def get_all_photos(self):
        '''Return  QuerySet of all photos related to this ost'''
        photos = Photo.objects.filter(post=self)  # photos tied to this profile
        return photos

    def get_absolute_url(self):
        '''Return  URL to display one instance of this Post'''
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_all_posts(self):
        '''Return a QuerySet of all Posts for profile, new first'''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')  # this profile's posts newest first
        return posts

    def get_followers(self):
        '''Return a list of Profiles who follow this profile'''
        follows = Follow.objects.filter(profile=self)  # follow rows pointing at this profile
        return [f.follower_profile for f in follows]  # pull out the follower profiles

    def get_num_followers(self):
        '''Return the count of followers for this profile'''
        return len(self.get_followers())  # how many followers

    def get_following(self):
        '''Return a list of Profiles that this profile follows'''
        follows = Follow.objects.filter(follower_profile=self)  # follow rows started by this profile
        return [f.profile for f in follows]  # pull out the followed profiles

    def get_num_following(self):
        '''Return the count of profiles this profile is following'''
        return len(self.get_following())  # how many profiles are followed

    def get_post_feed(self):
        '''Return a QuerySet of Posts from the profiles this profile follows, newest first'''
        following = self.get_following()  # profiles this user follows
        posts = Post.objects.filter(profile__in=following).order_by('-timestamp')  # their posts newest first
        return posts

class Post(models.Model):
    '''Encapsulate the data of an Instagram post'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)  # profile that made the post
    timestamp = models.DateTimeField(auto_now=True)  # when the post was made
    caption = models.TextField(blank=True)  # text caption for the post

    def __str__(self):
        return f'{self.caption}'

    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)  # photos attached to this post
        return photos

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'pk': self.pk})

    def get_all_comments(self):
        '''Return a QuerySet of all Comments on this Post'''
        comments = Comment.objects.filter(post=self)  # comments left on this post
        return comments

    def get_likes(self):
        '''Return a QuerySet of all Likes on this Post'''
        likes = Like.objects.filter(post=self)  # likes left on this post
        return likes

class Photo(models.Model):
    '''Encapsulate image associated with post'''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)  # post this photo belongs to
    image_url = models.URLField(blank=True)  # link to a hosted image
    image_file = models.ImageField(upload_to='', blank=True)  # uploaded image file
    timestamp = models.DateTimeField(auto_now=True)  # when the photo was added

    def __str__(self):
        '''Return a string representation of this photo'''
        if self.image_file:
            return f'{self.image_file.url}'
        return f'{self.image_url}'

    def get_image_url(self):
        '''Return the URL for this image'''
        if self.image_url:  # prefer the hosted url if present
            return self.image_url
        return self.image_file.url  # otherwise use the uploaded file

class Follow(models.Model):
    '''Encapsulate one Profile following another Profile'''
    profile = models.ForeignKey("Profile", related_name="profile", on_delete=models.CASCADE)  # profile being followed
    follower_profile = models.ForeignKey("Profile", related_name="follower_profile", on_delete=models.CASCADE)  # profile doing the following
    timestamp = models.DateTimeField(auto_now=True)  # when the follow started

    def __str__(self):
        '''Return a string representation of this Follow relationship'''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'

class Comment(models.Model):
    '''Encapsulate a Comment made by a Profile on a Post'''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)  # post being commented on
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)  # profile doing the commenting
    timestamp = models.DateTimeField(auto_now=True)  # when the comment was made
    text = models.TextField(blank=False)  # body of the comment

    def __str__(self):
        '''Return a string representation of this Comment'''
        return f'{self.profile.username}: {self.text}'

class Like(models.Model):
    '''Encapsulate a Like made by a Profile on a Post'''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)  # post being liked
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)  # profile doing the liking
    timestamp = models.DateTimeField(auto_now=True)  # when the like was made

    def __str__(self):
        '''Return a string representation of this Like'''
        return f'{self.profile.username} likes {self.post}'
