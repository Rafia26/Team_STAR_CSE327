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

def search_doctors_form(request):
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
          This method is used to search doctors based on the category inserted by user; it searches all
          the records in the database's child for the specialties and display the information.


          :param request: It is a HttpResponse from user.


          :type request: HttpResponse.


          :return: This method returns a html page that displays of the search for doctors from the database.


          :rtype: HttpResponse.
          """
    specialties = request.POST.get('specialties')
    docName = request.POST.get('docName')
 
    # If no input is given, then render to searchform.html
    if specialties or docName =="":
        return render(request, "searchform.html")
    if specialties is None or docName is None:
        print(docName ,"Name",specialties)
        return render(request, "searchform.html")
    else:
        if specialties == "Cardiologist" or "Neurologist" or "Dermatologist" or "Internist" or "Gynaecologist":
            data = database.child("Specialties").child(specialties).shallow().get().val()
            uidlist = []
            requid = 'null'
              
            # appending all the id in uidlist
            for i in data:
                uidlist.append(i)
                  
            # looking for the desired uid among all     
            for i in uidlist:
                fName = database.child("Specialties").child(specialties).child(i).child("fname").get().val()
                lName = database.child("Specialties").child(specialties).child(i).child("lname").get().val()
                name=fName + " " +lName 
                name=name.lower()
                docName=docName.lower()
                print(name,docName)
                  
                
                # storing that uid in requid
                if (name == docName):
                    requid = i
            if requid=='null':
                return render(request, "searchform.html")
            print(requid)
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
                           docFees
                           )
              
            
            # Sending all data in zip form to search.html        
            return render(request,'search/search.html',{"comb_lis": comb_lis})
    



