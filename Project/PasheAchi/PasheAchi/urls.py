"""PasheAchi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from LogInRegister import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('contact_us/', views.contact_us, name="contact_us"),
    path('description/', views.description, name="description"),
    path('about_us/', views.about_us, name="about_us"),
    path('google_login/', views.google_login, name="google_login"),
    path('home/', views.home, name="home"),
    path('patient_signup/', views.patient_signup, name="patient_signup"),
    path('doctor_signup/', views.doctor_signup, name="doctor_signup"),
    path('patient_post_signup/', views.patient_post_signup, name="patient_post_signup"),
    path('doctor_post_signup/', views.doctor_post_signup, name="doctor_post_signup"),
    path('logout/', views.logout, name="logout"), 
    path('forget_password/', views.forget_password, name = "forget_password"),   
    path('makeAp/', include('makeAppointment.urls')),
    path('viewAp/', include('viewAppointment.urls')),
    path('search/', include('search.urls')),
    path('donate/', include('donate.urls')),
    
    
    
    
]
