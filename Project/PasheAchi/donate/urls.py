from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [    
    
    path('donationform/', views.donation_form, name = "donationForm"),    
    path('donation/', views.donation, name = "donation"),    
]