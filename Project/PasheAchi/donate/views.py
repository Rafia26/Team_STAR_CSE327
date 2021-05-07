from django.shortcuts import render
from donate.models import Donation
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.http import HttpResponse

import pyrebase
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

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
storage = firebase.storage()
database = firebase.database()

def donation_form(request):
    """
        This method is used to display the donation form.


        :param request: It is a HttpResponse from user.


        :type request: HttpResponse.


        :return: This method returns a html page. It returns the form for inserting relevant donation information.


        :rtype: HttpResponse.
    """
    
    return render(request, "donate/donationform.html")

def donation(request):
    """
        This method is used to retrieve the relevant user inserted value from the donation form.

        It stores the retrieved data in the database.

        It sends an email confirmation about receiving of the donation form.

        :param request: It is a HttpResponse from user.

        :type request: HttpResponse.

        :return: This method returns a html page which displays the donation received confirmation message.

        :rtype: HttpResponse.

    """
    import time
    import pytz

    tz = pytz.timezone('Asia/Dhaka')
    timeNow = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(timeNow.timetuple()))

    donorName = request.POST.get('name')
    contactNum = request.POST.get('contactNum')
    email = request.POST.get('email')
    amount = request.POST.get('amount')
    trxId = request.POST.get('trxId')
  
    data = {
        'donorName':donorName, 'contactNum':contactNum, 'email':email,
        'amount':amount, 'trxId':trxId
        }

    database.child("Donation").child(millis).set(data)

    subject = 'Pashe Achi Donation'
    message = 'Hello {}. Pashe Achi has received your donation form. Your payment will be confirmed shortly via a phone call. Thank you so much for supporting our venture.'.format(donorName)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)


    return render(request, 'donate/confirmation.html', {'donorName':donorName})
    
