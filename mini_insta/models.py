from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a instagram profile '''
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this profile'''
        return f'{self.username} ({self.display_name})'
    
    def get_all_photos(self):
        '''Return  QuerySet of all photos related to this ost'''
        photos = Photo.objects.filter(post=self)
        return photos

    def get_absolute_url(self):
        '''Return  URL to display one instance of this Post'''
        return reverse('show_post', kwargs={'pk': self.pk})

    def get_all_posts(self):
        '''Return a QuerySet of all Posts for profile, new first'''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

class Post(models.Model):
    '''Encapsulate the data of an Instagram post'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f'{self.caption}'

    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'pk': self.pk})

class Photo(models.Model):
    '''Encapsulate image associated with post'''
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to='', blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this photo'''
        if self.image_file:
            return f'{self.image_file.url}'
        return f'{self.image_url}'
    
    def get_image_url(self):
        '''Return the URL for this image'''
        if self.image_url:
            return self.image_url
        return self.image_file.url