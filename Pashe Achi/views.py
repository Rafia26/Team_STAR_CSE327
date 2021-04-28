from django.shortcuts import render
from pyrebase import pyrebase

config={
    'apiKey': "AIzaSyBjmigr2xdarLAQhxdyN8jNKSEktJO3P2k",
    'authDomain': "projectpa-d8185.firebaseapp.com",
    'databaseURL': "https://projectpa-d8185-default-rtdb.firebaseio.com/",
    'projectId': "projectpa-d8185",
    'storageBucket': "projectpa-d8185.appspot.com",
    'messagingSenderId': "775438006449",
  };
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()