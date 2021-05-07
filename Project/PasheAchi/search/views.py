from django.shortcuts import render
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

def search_form(request):
    """
        This method is used to display search for doctors form.


        :param request: It is a HttpResponse from user.


        :type request: HttpResponse.


        :return: This method returns a html page. It returns the form for searching doctors.


        :rtype: HttpResponse.
        """
       
        
        
    return render(request, 'search/searchform.html')

def search(request):

    """
        This method is used to get the specialty and doctor's name from the search html form. 

        By matching the specialty and name, it retrieves doctor's information from database to display in the results.

        :param request: It's a HttpResponse from user.

        :type request: HttpResponse.

        :return: This method returns a html page that displays the search results.

        :rtype: HttpResponse.
    """
    specialties = request.POST.get('specialties')
    docName = request.POST.get('docName')
    docName=docName.lower()
 

    if specialties == "Cardiologist" or "Neurologist" or "Dermatologist" or "Internist" or "Gynaecologist":
        timeStamp = database.child("Specialties").child(specialties).get()
    timeStampList = []
    for i in timeStamp.each():
        timeStampKey = i.key()
        timeStampList.append(timeStampKey)
    
    for i in timeStampList:
        fName = database.child("Specialties").child(specialties).child(i).child("fname").get().val()
        lName = database.child("Specialties").child(specialties).child(i).child("lname").get().val()
        name=fName + " " +lName 
        name=name.lower()
   
        # storing the desired uid in requid
        if (name == docName):
            requid = i
            
            
    fName = database.child("Specialties").child(specialties).child(requid).child("fname").get().val()
    lName = database.child("Specialties").child(specialties).child(requid).child("lname").get().val()
    docGender = database.child("Specialties").child(specialties).child(requid).child("gender").get().val()
    docDesignation = database.child("Specialties").child(specialties).child(requid).child("designation").get().val()
    email = database.child("Specialties").child(specialties).child(requid).child("email").get().val()
    workplace = database.child("Specialties").child(specialties).child(requid).child("wplace").get().val()
    consultationHour1 = database.child("Specialties").child(specialties).child(requid).child("timeOne").get().val()
    consultationHour2 = database.child("Specialties").child(specialties).child(requid).child("timeTwo").get().val()
    fees = database.child("Specialties").child(specialties).child(requid).child("vfees").get().val()
            
    firstName = []
    firstName.append(fname)
    lastName = []
    lastName.append(lname)
    gender = []
    gender.append(docGender)
    designation = []
    designation.append(docDesignation)
    docEmail = []
    docEmail.append(email)
    docWorkplace = []
    docWorkplace.append(workplace)
    time1 = []
    time1.append(consultationHour1)
    time2 = []
    time2.append(consultationHour2)
    docFees = []
    docFees.append(fees)
            
    comb_lis = zip(firstName, lastName, 
                gender, designation, 
                docEmail, docWorkplace, 
                time1, time2, 
                docFees)
              
            
     # Sending all data in zip form to search.html        
    return render(request,'search/search.html',{"comb_lis": comb_lis})
    



