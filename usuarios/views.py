from django.shortcuts import render, redirect
from .models import Usuario

# Create your views here.
#vista de login
def loginView(request):
    if request.method=="POST":
        correo = request.POST.get("correo")
        password = request.POST.get("pass")
        usuario= Usuario.objects(correo=correo).first()
        if usuario:
            if usuario.check_password(password):
                request.session['user_email']= correo
                request.session.set_expiry(60*60*24*7*2)
                return redirect('')
            else:
                return render(request, 'usuarios/login.html', {'error': 'Usario o contraseña incorrecta'})
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usario o contraseña incorrecta'})
    else:
        return render(request, 'usuarios/login.html', {})

def registerView(request):
    if request.method=="POST":
        correo = request.POST.get("correo")
        password = request.POST.get("pass")
        password2= request.POST.get("pass2")
        #Verificar si correo ya está registrado
        if Usuario.objects(correo=correo).first():
            return render(request, 'usuarios/register.html', {'error': 'Usario ya existe'})
        #Si no, registramos usuario
        if password!=password2:
            return render(request, 'usuarios/register.html', {'error': 'Contraseñas deben coincidir'})
        usuario = Usuario(correo=correo)
        #cifrar contraseña
        usuario.set_password(password)
        usuario.save()
        return redirect('login')
    else:    
        return render(request, 'usuarios/register.html', {})
    
def logoutView(request):
    request.session.flush()
    return redirect("login")    