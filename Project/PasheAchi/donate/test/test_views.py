from django.contrib.sessions.middleware import SessionMiddleware
from donate.views import donation
from donate.views import donation_form
from donate.models import Donation
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
    ('donationForm'),
    ('donation')
])
def test_pageload(client, param):
    path = reverse('donation')
    assert resolve(path).view_name == "donation"
    path = reverse('donationForm')
    assert resolve(path).view_name == "donationForm"

@pytest.mark.parametrize('param', [
    ('donationForm'),
    ('donation')
])
def test_donation(client, param, user_data):
    view_url = urls.reverse('donationForm')
    print(view_url)
    response = client.post(view_url, data=user_data)
    assert "donationForm",{'donorName':donorName} in response.url

