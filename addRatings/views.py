from django.shortcuts import render, redirect
from addRatings.models import Ratings
from django.conf import settings
from django.core.mail import send_mail

import pyrebase
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

def star_rating_form(request):
    """
    This method is used to get the values from the star rating form to store data of the
    three types of ratings of each doctor in the database.
    And it sends email confirmation of ratings submission to the patient.

     :param request: it's a HttpResponse from user.

     :type request: HttpResponse.

     :return: this method redirects us to another method/def:page
                that will display the rating form confirmation message.

     :rtype: HttpResponse.
    """
    doctorId = request.POST.get('doctorId')
    serviceR = request.POST.get('serviceR')
    behaviourR = request.POST.get('behaviourR')
    accdR = request.POST.get('accdR')
    # idtoken = request.session['LoginId']
    # a = authe.get_account_info(idtoken)
    # a = a['users']
    # a = a[0]
    # a = a['localId']
    a = "6ktQk2bH3ZddF4suT8LRS3xlXJ83"
    data = {
        'patientId': a,
        'doctorId': doctorId,
        'serviceR': serviceR,
        'behaviourR': behaviourR,
        'accdR': accdR,
    }
    doctorFirstName = database.child("Users").child("Doctor").child(doctorId).child("fname").get().val()
    doctorLastName = database.child("Users").child("Doctor").child(doctorId).child("lname").get().val()
    patientFirstName = database.child("Users").child("Patient").child(a).child("fname").get().val()
    patientLastName = database.child("Users").child("Patient").child(a).child("lname").get().val()
    patientEmail = database.child("Users").child("Patient").child(a).child("email").get().val()
    subject = 'Pashe Achi Ratings Confirmation'
    message = 'Hello {} {}, Your rating confirmation of {} {} is done.'.format(patientFirstName, patientLastName,
                                                                               doctorFirstName, doctorLastName)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [patientEmail]
    send_mail(subject, message, email_from, recipient_list)
    patientFirstName = database.child("Users").child("Patient").child(a).child("fname").get().val()
    patientLastName = database.child("Users").child("Patient").child(a).child("lname").get().val()
    database.child("Ratings").child(doctorId).set(data)

    # return render(request, 'addRatings/confirmRatings.html', {'patientFirstName': patientFirstName},
    #               {'patientLastName': patientLastName})
    return redirect("page")

def page(request):
    """
    This method is used to render the values from star_rating_form and
    send to confirm the ratings.

     :param request: it's a HttpResponse from user.

     :type request: HttpResponse.

     :return: this method returns a html page that displays the rating form confirmation message.

     :rtype: HttpResponse.
    """
    a = "6ktQk2bH3ZddF4suT8LRS3xlXJ83"
    patientFirstName = database.child("Users").child("Patient").child(a).child("fname").get().val()
    patientLastName = database.child("Users").child("Patient").child(a).child("lname").get().val()
    return render(request, 'addRatings/confirmRatings.html',
                  {'patientFirstName': patientFirstName, 'patientLastName': patientLastName})

def confirm_star_rating(request):
    """
         This method is used to retrieve doctor's name and each of the three ratings from database
         to display in the ratings form.

         :param request: it's a HttpResponse from user.

         :type request: HttpResponse.

         :return: this method returns a html page that displays the ratings form.

         :rtype: HttpResponse.
    """
    docId = database.child("Users").child("Doctor").get()
    docIdList = []
    for i in docId.each():
        docIdKey = i.key()
        docIdList.append(docIdKey)
    doctorNameList = []
    doctorId = []
    serviceRList = []
    behaviourRList = []
    accdRList = []
    for i in docIdList:
        tempDoctorName = database.child("Users").child("Doctor").child(i).child("fname").get().val()
        doctorNameList.append(tempDoctorName)
        tempServiceR = database.child("Ratings").child("Doctor").child(i).child("serviceR").get().val()
        serviceRList.append(tempServiceR)
        tempBehaviourR = database.child("Ratings").child("Doctor").child(i).child("behaviourR").get().val()
        behaviourRList.append(tempBehaviourR)
        tempAccdR = database.child("Ratings").child("Doctor").child(i).child("accdR").get().val()
        accdRList.append(tempAccdR)
        dId = i
        doctorId.append(dId)
    allDoctorName = zip(doctorNameList, doctorId)
    ratings = zip(doctorId, serviceRList, behaviourRList, accdRList)
    if star_rating_form:
        return render(request, 'addRatings/addRatings.html', {'allDoctorName': allDoctorName, 'ratings': ratings})
