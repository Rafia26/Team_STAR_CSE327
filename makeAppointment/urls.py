from django.urls import path
from . import views

urlpatterns = [
    path('appForm/', views.appointment_form, name = "appForm"),
    path('createAppointment/', views.create_appointment, name = "createAppointment"),
    path('appointment_form_redirect/', views.appointment_form_redirect, name = "appointment_form_redirect"),
    path('create_appointment_redirect/', views.create_appointment_redirect, name = "create_appointment_redirect")
]