
from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('subscribe/<str:membership>/', views.subscribe, name='subscribe_with_membership'),
    path('services', views.services, name='services'),
    path('team', views.team, name='team'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('create_account', views.create_account, name='create_account'),

]
