from django.contrib import admin
from django.urls import path
from landing import views as landingViews
from usuarios import views as usuariosViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landingViews.index, name=''),
    path('sobreNosotros', landingViews.aboutUs, name="aboutUs"),
    path('contactanos', landingViews.contact, name="contact"),
    path('login', usuariosViews.loginView, name='login'),
    path('register', usuariosViews.registerView, name='register'),
    path('logout', usuariosViews.logoutView, name='logout'),
    path('passRecovery', usuariosViews.recuperarPass, name='recuperar'),
    path("verificar-codigo/", usuariosViews.verificar_codigo, name="verificar_codigo"),
    path('resetPassword', usuariosViews.resetPassword, name="resetPassword")
]
