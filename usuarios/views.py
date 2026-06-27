from django.shortcuts import render, redirect
from .models import Usuario, PasswordResetCode
import string
import secrets
from django.http import JsonResponse
from django.utils import timezone
import time

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

def recuperarPass(request):
    if request.method=="POST":
        correo = request.POST.get("correo")
        #Verificar si correo ya está registrado
        if Usuario.objects(correo=correo).first():
            #Manda correo
            codigo = ''.join(secrets.choice(string.digits) for _ in range(6))
            
            # guardar y borrar codigos anteriores
            PasswordResetCode.objects(correo=correo).delete()

            reset = PasswordResetCode(correo=correo)
            reset.set_codigo(codigo)
            reset.save()

            print("CODIGO:", codigo)
            return JsonResponse({"ok": True})
        else:     
            return JsonResponse({"ok": False, "error": "Usuario no encontrado"})
    else:
        return render(request, 'usuarios/recuperarPass.html', {})
    
def verificar_codigo(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        codigo = request.POST.get("codigo")

        reset = PasswordResetCode.objects(correo=correo).first()

        if not reset:
            return JsonResponse({
                "ok": False,
                "error": "Código no encontrado o expirado"
            })

        # validar código
        if reset.check_codigo(codigo):
            # opcional: eliminar después de usarlo (recomendado)
            reset.delete()
            request.session["correo"]=correo
            request.session["password_reset_allowed"] = True
            request.session["password_reset_time"] = time.time()

            return JsonResponse({
                "ok": True,
                "message": "Código válido"
            })

        return JsonResponse({
            "ok": False,
            "error": "Código incorrecto"
        })

    return JsonResponse({
        "ok": False,
        "error": "Método no permitido"
    })    

def resetPassword(request):
    allowed = request.session.get("password_reset_allowed", False)
    timestamp = request.session.get("password_reset_time", None)

    if not allowed or not timestamp:
        return redirect("login")
    
    if time.time() - timestamp > 300:
        request.session.pop("password_reset_allowed", None)
        request.session.pop("password_reset_time", None)

        return redirect("login")
    
    if request.method == "POST":
        correo= request.session.get("correo")
        password = request.POST.get("pass")
        password2= request.POST.get("pass2")
        if password!=password2:
            return render(request, 'usuarios/recuperarPass.html', {'error': 'Contraseñas deben coincidir'})
        usuario = Usuario.objects(correo=correo).first()
        #cifrar contraseña
        usuario.set_password(password)
        usuario.save()
        return redirect('login')


    return render(request, "usuarios/resetPassword.html")