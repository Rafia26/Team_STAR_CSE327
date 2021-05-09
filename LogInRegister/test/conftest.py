from django.contrib.sessions.middleware import SessionMiddleware
from LogInRegister.models import LogIn
from LogInRegister.views import post_login
from LogInRegister.views import patient_post_signup
from LogInRegister.views import psignup_test
from LogInRegister.views import doctor_post_signup
from LogInRegister.views import dsignup_test
from LogInRegister.views import login_test
from django.http import request, response
from django.urls import reverse, resolve
from django.test import RequestFactory
from django.shortcuts import render
from django.conf import settings
from django import urls
import pyrebase
import pytest
import os

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

@pytest.fixture
def user_data():
	return { 'email': 'ktjt.0301@gmail.com',
    'password': '123456'
}

@pytest.fixture
def p_data():
	return { 'userFname': "Hello Unit",
    'userLname': "Testing",
    'userAge': "21",
    'userDob': "2000-01-01",
    'userGender': "Others", 
    'userOccupation': "Pytest",
    'userCnumber': "01671406838",
    'userBgroup': "B+",
    'userEmail': "ktjt.0301@gmail.com",
    'userPassword': "123456",
    'userCPassword': "123456",
}

@pytest.fixture
def d_data():
	return { 'userFname':  "Dr. Unit",
    'userLname': "Testing",
    'userAge':  "21",
    'userDob':  "2000-01-01",
    'userGender':  "Others",
    'userSpecializedField':  "Pytest",
    'userDesignation':  "Test Project", 
    'userWorkingPlace':  "Testing Medical",
    'userWorkingHour1':  "12:30",
    'userWorkingHour2':  "23:00", 
    'userVisitingFees':  "2000",
    'userCnumber':  "01671406838", 
    'userBgroup':  "A-",
    'userEmail': "ktjt.0301@gmail.com",
    'userPassword': "123456",
    'userCPassword': "123456",
}



