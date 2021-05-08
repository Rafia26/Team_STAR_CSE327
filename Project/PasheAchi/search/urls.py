from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    
    path('searchform/', views.search_form,name="searchForm"), 
    path('search/', views.search, name="search"), 
    path('searchnotfound/',views.search_not_found, name="searchnotfound"),
    
]