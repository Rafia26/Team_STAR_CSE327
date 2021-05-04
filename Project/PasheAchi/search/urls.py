from django.urls import path

from . import views

urlpatterns = [
"""
Url for search form
"""
    path('searchform/', views.searchform,name="searchForm"),

"""
    Showing search detail on this url
"""
    path('search/', views.search, name="search"),
    
]