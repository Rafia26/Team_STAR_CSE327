from django.urls import path
from . import views

urlpatterns = [
    path('appoints/', views.appointments, name = "viewAppointments"),
    path('cancelAppointments/<int:timeStampList>/',views.cancel_appointment, name = "cancelAppointments")
]