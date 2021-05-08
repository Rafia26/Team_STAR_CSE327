from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    """
        Url for search form.
    """
    path('searchform/', views.search_form,name="searchForm"),

    """
        Showing search detail on this url.
    """
    path('search/', views.search, name="search"),
    
    """
        Url in case search results are not found.
    """  
    path('searchnotfound/',views.search_not_found, name="searchnotfound"),
    
]