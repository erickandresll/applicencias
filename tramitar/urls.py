from django.contrib import admin
from django.urls import path
from tramitar import views

urlpatterns = [
        path('index/', views.load_licencias, name='index'),
        path('loadlicencias/', views.load_licencias, name='loadlicencias'),
        path('cargar/', views.carga_archivos, name='cargar_archivos'),
]
