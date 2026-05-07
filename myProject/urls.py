"""
URL configuration for myProject project.
"""
from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('privacy', views.privacy, name='privacy'),
    path('privacy/', views.privacy),
    path('terms', views.terms, name='terms'),
    path('terms/', views.terms),
    path('security', views.security, name='security'),
    path('security/', views.security),
    path('data-deletion', views.data_deletion, name='data_deletion'),
    path('data-deletion/', views.data_deletion),
    path('contact', views.contact, name='contact'),
    path('contact/', views.contact),
    path('login', views.login_page, name='login'),
    path('login/', views.login_page),
    path('signup', views.signup_page, name='signup'),
    path('signup/', views.signup_page),
    path('launchpad', views.launchpad, name='launchpad'),
    path('launchpad/', views.launchpad),
    path('logout', views.logout_view, name='logout'),
    path('logout/', views.logout_view),
]
