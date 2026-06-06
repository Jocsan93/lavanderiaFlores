from django.shortcuts import render

# Create your views here.
#vista de login
def loginView(request):
    return render(request, 'usuarios/login.html', {})

def registerView(request):
    return render(request, 'usuarios/register.html', {})