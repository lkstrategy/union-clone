from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('<int:lead_id>', views.leadCompleteView, name='leadCompleteView'),
    url(r'^ajax/ajax_change_status/$', views.ajax_change_status, name='ajax_change_status'),
    url(r'^ajax/ajax_get_news/$', views.ajax_get_news, name='ajax_get_news'),
    url(r'^ajax/ajax_update_lead_status/$', views.ajax_update_lead_status, name='ajax_update_lead_status'),
    url(r'^ajax/ajax_update_lead_archived/$', views.ajax_update_lead_archived, name='ajax_update_lead_archived'),
]