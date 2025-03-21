from django.contrib import admin
from django.urls import path
from winbuzzSS import views

urlpatterns = [
    path('', views.firstPage, name="FirstPage"),
    path('download/', views.download_image, name="downloadImage"),
]
