from django.shortcuts import render

def index(request):
    return render(request, 'landing/index.html', {})

def aboutUs(request):
    return render(request, 'landing/aboutUs.html', {})

def contact(request):
    return render(request, 'landing/contact.html', {})