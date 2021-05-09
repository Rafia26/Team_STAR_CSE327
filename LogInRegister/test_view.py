from django.contrib.sessions.middleware import SessionMiddleware
from LogInRegister.views import post_login
from LogInRegister.views import login_test
from LogInRegister.views import patient_post_signup
from LogInRegister.views import psignup_test
from LogInRegister.views import doctor_post_signup
from LogInRegister.views import dsignup_test
from LogInRegister.models import LogIn
from django.http import request, response
from django.urls import reverse, resolve
from django.test import RequestFactory
from django.shortcuts import render
from django.conf import settings
from django import urls
import pyrebase
import pytest
import os

from django.http import HttpResponse
config={
    "apiKey": "AIzaSyD-ndCLqY-TtlabOCyy1-t0AN_O7yz7zGo",
    "authDomain": "pashe-achi.firebaseapp.com",
    "databaseURL": "https://pashe-achi-default-rtdb.firebaseio.com/",
    "projectId": "pashe-achi",
    "storageBucket": "pashe-achi.appspot.com",
    "messagingSenderId": "1005617401533",
    "appId": "1:1005617401533:web:1d756003c3bd2e8b0f71d4",
    "measurementId": "G-QR9VX6SRV4"
}

"""
Global Variables
"""
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
storage = firebase.storage()
database = firebase.database()

@pytest.mark.parametrize('param', [
    ('home'), ('google_login'), ('post_login'), 
    ('patient_signup'), ('doctor_signup'), 
    ('patient_post_signup'), ('doctor_post_signup'),
    ('logout'), ('forget_password'),
    ('about_us'), ('contact_us'), ('description')
])

def test_page(param):
    """
    This method is used for unit testing the pages.
    """
    path = reverse('home') 
    assert resolve(path).view_name == "home"

    path = reverse('google_login') 
    assert resolve(path).view_name == "google_login"
    
    path = reverse('post_login') 
    assert resolve(path).view_name == "post_login"
    
    path = reverse('patient_signup') 
    assert resolve(path).view_name == "patient_signup"

    path = reverse('doctor_signup') 
    assert resolve(path).view_name == "doctor_signup"

    path = reverse('patient_post_signup') 
    assert resolve(path).view_name == "patient_post_signup"

    path = reverse('doctor_post_signup') 
    assert resolve(path).view_name == "doctor_post_signup"

    path = reverse('logout') 
    assert resolve(path).view_name == "logout"

    path = reverse('forget_password') 
    assert resolve(path).view_name == "forget_password"

    path = reverse('about_us') 
    assert resolve(path).view_name == "about_us"

    path = reverse('contact_us') 
    assert resolve(path).view_name == "contact_us"

    path = reverse('description') 
    assert resolve(path).view_name == "description"

@pytest.mark.parametrize('param', [
    ('post_login'),
])
def test_login(client, param,  user_data):
    """
    This method is used for unit testing login.
    """
    view_url = urls.reverse('post_login')
    response = client.post(view_url, data=user_data)
    assert "login_test" in response.url

@pytest.mark.parametrize('param', [
    ('patient_post_signup'),
])
def test_psignup(client, param,  p_data):
    """
    This method is used for unit testing patient signup.
    """
    view_url = urls.reverse('patient_post_signup')
    response = client.post(view_url, data=p_data)
    assert "psignup_test" in response.url

@pytest.mark.parametrize('param', [
    ('doctor_post_signup'),
])
def test_dsignup(client, param,  d_data):
    """
    This method is used for unit testing doctor signup.
    """
    view_url = urls.reverse('doctor_post_signup')
    response = client.post(view_url, data=d_data)
    assert "dsignup_test" in response.url