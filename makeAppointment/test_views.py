from django.contrib.sessions.middleware import SessionMiddleware
from makeAppointment.views import create_appointment
from makeAppointment.views import appointment_form
from makeAppointment.models import Appointment
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
    ('createAppointment'),
    ('appForm')
])
def test_page(client, param):
    """
    This method is used for unit testing.
    """
    path = reverse('createAppointment')
    assert resolve(path).view_name == "createAppointment"
    path = reverse('appForm')
    assert resolve(path).view_name == "appForm"

def test_appointment(client, user_data):
    """
    This method is used for unit testing.
    """
    view_url = urls.reverse('appForm')
    response = client.post(view_url, data=user_data)
    assert "appForm",{'patientName':patientName} in response.url

def test_create_appointment(client):
    """
    This method is used for unit testing.
    """
    view_url = urls.reverse('createAppointment')
    response = client.post(view_url)
    assert "createAppointment",{'allDoctorName':allDoctorName,'timeSlot':timeSlot} in response.url