from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a instagram profile. '''
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this profile.'''
        return f'{self.username} ({self.display_name})'