# File: forms.py
# Author: Ignacio Fernandez, ifw@bu.edu
# Description: defines the form classes for the mini_insta application
from django import forms
from .models import Post, Profile


class CreatePostForm(forms.ModelForm):
    '''A form to create a new Post.'''
    class Meta:
        model = Post  # model this form edits
        fields = ['caption']  # editable fields

class UpdateProfileForm(forms.ModelForm):
    '''Form to update a profile.'''
    class Meta:
        model = Profile  # model this form edits
        fields = ['display_name', 'profile_image_url', 'bio_text']  # editable fields

class UpdatePostForm(forms.ModelForm):
    '''Form to update an existing Post.'''
    class Meta:
        model = Post  # model this form edits
        fields = ['caption']  # editable fields
