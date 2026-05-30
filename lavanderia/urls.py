from django.contrib import admin
from django.urls import path
from landing import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name=''),
    path('sobreNosotros', views.aboutUs, name="aboutUs"),
    path('contactanos', views.contact, name="contact"),
]
