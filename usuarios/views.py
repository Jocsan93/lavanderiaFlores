from django.shortcuts import render, redirect
from .models import Usuario, PasswordResetCode
import string
import secrets
from django.http import JsonResponse
from django.utils import timezone
import time
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings

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
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()

        # Verificar usuario
        user = Usuario.objects(correo=correo).first()

        if user:

            # borrar códigos anteriores
            PasswordResetCode.objects(correo=correo).delete()

            # generar código
            codigo = ''.join(secrets.choice(string.digits) for _ in range(6))

            reset = PasswordResetCode(correo=correo)
            reset.set_codigo(codigo)
            reset.save()

            # sesión (opcional pero útil)
            request.session["reset_email"] = correo

            # conexión SMTP explícita (como tu ejemplo)
            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
                fail_silently=False,
                local_hostname="uth.hn"
            )

            # HTML del correo (mejorado estilo cajas por dígito)
            cajas = "".join([
                f"""
                <span style="
                    display:inline-block;
                    width:55px;
                    height:70px;
                    line-height:70px;
                    margin:4px;
                    background:#eef2f7;
                    border:2px solid #2c3e50;
                    border-radius:8px;
                    font-size:36px;
                    font-weight:bold;
                    color:#2c3e50;
                    text-align:center;
                ">
                    {d}
                </span>
                """
                for d in codigo
            ])

            html_content = f"""
            <div style="font-family: Arial, sans-serif; background-color:#f4f6f8; padding:30px;">
                <div style="
                    max-width:500px;
                    margin:auto;
                    background:white;
                    padding:30px;
                    border-radius:10px;
                    box-shadow:0 2px 10px rgba(0,0,0,0.1);
                    text-align:center;
                ">

                    <h2 style="color:#333;">Recuperación de contraseña</h2>

                    <p style="color:#555;">
                        Hemos recibido una solicitud para restablecer tu contraseña.
                    </p>

                    <div style="margin:30px 0;">
                        {cajas}
                    </div>

                    <p style="color:#666; font-size:14px;">
                        Si no fuiste tú, puedes ignorar este mensaje.
                    </p>

                    <hr style="margin:25px 0; border:none; border-top:1px solid #eee;">

                    <p style="font-size:12px; color:#999;">
                        Este es un mensaje automático, no respondas a este correo.
                    </p>

                </div>
            </div>
            """

            email = EmailMultiAlternatives(
                subject="Recuperación de contraseña",
                body=f"Tu código es: {codigo}",
                from_email=settings.EMAIL_HOST_USER,
                to=[correo],
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            return JsonResponse({"ok": True})

        return JsonResponse({"ok": False})

    return render(request, "usuarios/recuperarPass.html", {})
    
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