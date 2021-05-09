from django.shortcuts import render
from addRatings.models import Ratings
from django.conf import settings

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

def view_star_rating(request):
    """
         This method is used to retrieve star ratings from database
         to display each doctor's rating according to their
         service (serviceR), behaviour (behaviourR) and Accurate Diagnosis (accdR).

         :param request: It's a HttpResponse from user.

         :type request: HttpResponse.

         :return: If the database doesn't contain any ratings, it returns an HTML page
                    showing a text: "There are no ratings at the moment".
                Else,
                    If a patient is logged in, it returns an HTML page that displays doctor ratings.
                    If a doctor is logged in, it returns an HTML page that displays doctors ratings.
                    If there are no ratings, the logged in user will view an HTML page showing text.

         :rtype: HttpResponse.
    """
    idtoken = request.session['LoginId']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timeStamp = database.child("Ratings").get()
    if timeStamp is None:
        return render(request, 'viewRatings/viewRatings.html')
    else:
        timeStampList = []
        for i in timeStamp.each():
            timeStampKey = i.key()
            timeStampList.append(timeStampKey)
        doctorNameList1 = []
        doctorNameList2 = []
        serviceRList = []
        behaviourRList = []
        accdRList = []
        ratingDetails = []
        row = []
        rowNo = 0
        doctorIdView = None
        patientIdView = None
        for i in timeStampList:
            patientId = database.child("Ratings").child(i).child("patientId").get().val()
            doctorId = database.child("Ratings").child(i).child("doctorId").get().val()
            if (doctorId == a):
                doctorIdView = database.child("Ratings").child(i).child("doctorId").get().val()
                rowNo = rowNo + 1
                row.append(rowNo)
                tempServiceR = database.child("Ratings").child(i).child("serviceR").get().val()
                serviceRList.append(tempServiceR)
                tempBehaviourR = database.child("Ratings").child(i).child("behaviourR").get().val()
                behaviourRList.append(tempBehaviourR)
                tempAccdR = database.child("Ratings").child(i).child("accdR").get().val()
                accdRList.append(tempAccdR)
                tempDoctorFirstName = database.child("Users").child("Doctor").child(doctorId).child("fname").get().val()
                doctorNameList1.append(tempDoctorFirstName)
                tempDoctorLastName = database.child("Users").child("Doctor").child(doctorId).child("lname").get().val()
                doctorNameList2.append(tempDoctorLastName)
            elif (patientId == a):
                patientIdView = database.child("Ratings").child(i).child("patientId").get().val()
                rowNo = rowNo + 1
                row.append(rowNo)
                tempServiceR = database.child("Ratings").child(i).child("serviceR").get().val()
                serviceRList.append(tempServiceR)
                tempBehaviourR = database.child("Ratings").child(i).child("behaviourR").get().val()
                behaviourRList.append(tempBehaviourR)
                tempAccdR = database.child("Ratings").child(i).child("accdR").get().val()
                accdRList.append(tempAccdR)
                tempDoctorFirstName = database.child("Users").child("Doctor").child(doctorId).child("fname").get().val()
                doctorNameList1.append(tempDoctorFirstName)
                tempDoctorLastName = database.child("Users").child("Doctor").child(doctorId).child("lname").get().val()
                doctorNameList2.append(tempDoctorLastName)
        ratingDetails = zip(row, doctorNameList1, serviceRList, behaviourRList, accdRList)
        if (doctorIdView == a):
            doctorFirstName = database.child("Users").child("Doctor").child(a).child("fname").get().val()
            doctorLastName = database.child("Users").child("Doctor").child(a).child("lname").get().val()
            return render(request, 'viewRatings/viewRatings.html', {'ratingDetails': ratingDetails})
        elif (patientIdView == a):
            doctorFirstName = database.child("Users").child("Doctor").child(a).child("fname").get().val()
            doctorLastName = database.child("Users").child("Doctor").child(a).child("lname").get().val()
            return render(request, 'viewRatings/viewRatings.html', {'ratingDetails': ratingDetails})
        else:
            return render(request, "viewRatings/noRatings.html")
    return render(request, 'LogInRegister/home.html')
