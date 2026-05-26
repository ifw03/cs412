from django.shortcuts import render
import random
from datetime import datetime, timedelta
# Create your views here.

MENU = {
    'lomo':    ('Lomo Saltado',     14.00),
    'ceviche': ('Ceviche Clasico',  16.00),
    'pollo':   ('Pollo a la Brasa', 12.00),
    'causa':   ('Causa Limena',      9.00),
}

EXTRAS = {
    'extra_fries': ('Extra fries',   2.50),
    'fried_egg':   ('Fried egg',     1.50),
}

DAILY_SPECIALS = [
    {'name': 'Aji de Gallina',
     'price': 13.00,
     'description': 'Shredded chicken in a creamy yellow-chili sauce, with rice and potato.'},
    {'name': 'Anticuchos',
     'price': 11.00,
     'description': 'Grilled beef-heart skewers in a smoky panca-chili marinade.'},
    {'name': 'Tacu Tacu con Lomo',
     'price': 15.00,
     'description': 'Pan-fried rice and beans topped with thin steak and salsa criolla.'},
    {'name': 'Arroz con Mariscos',
     'price': 17.00,
     'description': 'Peruvian-style seafood rice cooked with aji amarillo and white wine.'},
]

def main(request):
    """Display the main page with restaurant info."""
    return render(request, 'restaurant/main.html')


def order(request):
    """Display the online order form with a random daily special."""
    context = {
        'special': random.choice(DAILY_SPECIALS),
    }
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    """Process a submitted order and display a confirmation page."""
    if request.method != 'POST':
        return render(request, 'restaurant/order.html',
                      {'special': random.choice(DAILY_SPECIALS)})
    ordered_items = []
    total = 0.0

    for key, (name, price) in MENU.items():
        if key in request.POST:
            ordered_items.append({'name': name, 'price': price})
            total += price

    for key, (name, price) in EXTRAS.items():
        if key in request.POST:
            ordered_items.append({'name': name, 'price': price})
            total += price

    if 'special' in request.POST:
        special_name = request.POST.get('special_name', 'Daily Special')
        special_price = float(request.POST.get('special_price', 0))
        ordered_items.append({
            'name': special_name + ' (Daily Special)',
            'price': special_price,
        })
        total += special_price

    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    instructions = request.POST.get('instructions', '')

    minutes = random.randint(30, 60)
    ready = datetime.now() + timedelta(minutes=minutes)
    readytime = ready.strftime('%I:%M %p')

    context = {
        'name': name,
        'phone': phone,
        'email': email,
        'instructions': instructions,
        'ordered_items': ordered_items,
        'total': total,
        'readytime': readytime,
    }
    return render(request, 'restaurant/confirmation.html', context)