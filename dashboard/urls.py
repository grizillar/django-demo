from django.urls import path, register_converter

from dashboard.scripts.converter import DateConverter

from . import views

register_converter(DateConverter, "date")

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('/?startdate=<date:sdate>&enddate=<date:edate>',
    #      views.dashboard, name='dashboard'),
    path('demo/', views.demo, name='demo'),
    path('upload/', views.upload, name='upload'),
    path('upload-success/', views.uploadsuccess, name='upload-success')

]
