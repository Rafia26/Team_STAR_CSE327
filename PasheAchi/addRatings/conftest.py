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


@pytest.fixture
def user_data():
    return {'accdR': '3.2', 'behaviourR': '2.5',
            'doctorId': 'mH7X1hCwCbS60PWJjRB6aKES0Wx2', 'serviceR': '1.5'}
