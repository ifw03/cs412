# File: views.py
# Author: Ignacio Fernandez, ifw@bu.edu
# Description: defines the view classes for the mini_insta application
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin  # gates views behind login
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    '''A LoginRequiredMixin that can also find the Profile of the logged-in User.'''

    def get_login_url(self):
        '''Return the URL of the login page.'''
        return reverse('login')  # send unauthenticated users to our login page

    def get_profile(self):
        '''Return the Profile associated with the logged-in User.'''
        return Profile.objects.filter(user=self.request.user).first()  # this user's profile

class ProfileListView(ListView):
    '''Display list of all profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Display single profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Display a single Post'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(ProfileLoginRequiredMixin, CreateView):
    '''Handle creation of a new Post .'''
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()  # the logged-in user's profile
        return context

    def form_valid(self, form):
        profile = self.get_profile()  # the logged-in user's profile
        form.instance.profile = profile  # attach the post to this profile
        # superclass saves the post and sets self.object
        response = super().form_valid(form)

        files = self.request.FILES.getlist('files')  # any uploaded image files
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)  # make a photo per file
        return response

class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView):
    '''view to update profile, save it to the database'''
    model = Profile                                       # model to update
    form_class = UpdateProfileForm                         # form used to collect updated data
    template_name = 'mini_insta/update_profile_form.html'  # template that renders the form

    def get_object(self):
        '''Return the Profile of the logged-in User.'''
        return self.get_profile()  # edit the logged-in user's own profile

class DeletePostView(ProfileLoginRequiredMixin, DeleteView):
    '''Handle deletion of an existing Post.'''
    model = Post                                          # model to delete
    template_name = 'mini_insta/delete_post_form.html'    # template that confirms the delete

    def get_context_data(self, **kwargs):
        '''Provide the Post and its Profile to the template.'''
        context = super().get_context_data(**kwargs)
        post = self.get_object()  # the post being deleted
        context['post'] = post
        context['profile'] = post.profile  # owner of the post
        return context

    def get_success_url(self):
        '''After deleting, redirect to the profile page of the Post's owner.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})  # back to owner profile

class UpdatePostView(ProfileLoginRequiredMixin, UpdateView):
    '''Handle updating the caption of an existing Post.'''
    model = Post                                          # model to update
    form_class = UpdatePostForm                            # form used to collect the new caption
    template_name = 'mini_insta/update_post_form.html'    # template that renders the form

class ShowFollowersDetailView(DetailView):
    '''Display the followers of a single Profile.'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''Display the profiles a single Profile is following.'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowMyProfileView(ProfileLoginRequiredMixin, DetailView):
    '''Display the logged-in user's own profile page.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Return the Profile of the logged-in User.'''
        return self.get_profile()  # show the logged-in user's own profile

class ShowFeedView(ProfileLoginRequiredMixin, DetailView):
    '''Display the post feed for the logged-in Profile.'''
    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Return the Profile of the logged-in User.'''
        return self.get_profile()  # feed belongs to the logged-in user

class SearchView(ProfileLoginRequiredMixin, ListView):
    '''Search Profiles and Posts based on a text query.'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Require login, then show the search form if there is no query.'''
        if not request.user.is_authenticated:
            # let the mixin handle the redirect to the login page
            return super().dispatch(request, *args, **kwargs)
        if 'query' not in self.request.GET:
            # no query yet: display the form to collect one
            profile = self.get_profile()  # logged-in user's profile for the template
            return render(request, 'mini_insta/search.html', {'profile': profile})
        # query present: let the generic ListView do its work
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return the Posts whose caption contains the query.'''
        query = self.request.GET.get('query')  # the text the user searched for
        posts = Post.objects.filter(caption__icontains=query)  # posts whose caption contains it
        return posts

    def get_context_data(self, **kwargs):
        '''Add the profile, query, matching posts, and matching profiles.'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')  # the text the user searched for
        context['profile'] = self.get_profile()  # logged-in user's profile
        context['query'] = query
        context['posts'] = self.get_queryset()  # matching posts
        # a profile matches on username, display name, or bio text
        by_username = Profile.objects.filter(username__icontains=query)  # match on username
        by_display = Profile.objects.filter(display_name__icontains=query)  # match on display name
        by_bio = Profile.objects.filter(bio_text__icontains=query)  # match on bio text
        context['profiles'] = (by_username | by_display | by_bio).distinct()  # combined, no duplicates
        return context
