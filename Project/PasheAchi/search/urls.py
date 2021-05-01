from django.urls import path

from . import views

urlpatterns = [
    path('searchForm/', views.search_doctors_form,name="searchForm"),
    path('search/', views.search, name="search"),
    
]