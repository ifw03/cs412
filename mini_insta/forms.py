from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    '''A form to create a new Post.'''
    class Meta:
        model = Post
        fields = ['caption']