from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('demo/', views.demo, name='demo'),
    path('upload/', views.upload, name='upload')


]
