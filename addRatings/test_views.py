from django.contrib.sessions.middleware import SessionMiddleware
from addRatings.views import confirm_star_rating
from addRatings.views import star_rating_form
from addRatings.models import Ratings
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

config = {
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
    ('confirm_r'),
    ('add_r')
])
def test_page(client, param):
    path = reverse('confirm_r')
    assert resolve(path).view_name == "confirm_r"
    path = reverse('add_r')
    assert resolve(path).view_name == "add_r"


@pytest.mark.parametrize('param', [
    ('add_r'),
    ('page')
])
def test_rating(client, param, user_data):
    view_url = urls.reverse('add_r')
    print(view_url)
    response = client.post(view_url, data=user_data)
    assert "add_r", {'patientFirstName': patientFirstName} in response.url
