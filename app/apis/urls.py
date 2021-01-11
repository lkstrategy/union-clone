from django.urls import path

from . import views

urlpatterns = [
    path('salesloftperson', views.salesloftperson, name='salesloftperson'),
    path('create', views.create_post, name='create'),
]