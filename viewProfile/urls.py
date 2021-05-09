from django.urls import path
from . import views

urlpatterns = [
    path('viewProfile/', views.view_profile, name = "viewProfile"),
    path('deleteProfile/', views.delete_profile, name = "deleteProfile")  
]