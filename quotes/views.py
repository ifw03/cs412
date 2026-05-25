from django.shortcuts import render
import random

quotes = [
    "Life is like riding a bicycle. To keep your balance, you must keep moving.",
    "Imagination is more important than knowledge.",
    "A person who never made a mistake never tried anything new.",
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/8/8a/Albert_Einstein_%28Nobel%29.png",
]

def quote(request):
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')
# Create your views here.
