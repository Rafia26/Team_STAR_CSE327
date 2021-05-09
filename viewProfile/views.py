from django.shortcuts import render
from LogInRegister.models import PatientSignUp
from LogInRegister.models import DoctorSignUp
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import auth
import pyrebase
import os

"""
Global Variables
"""
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

# Create your views here.

#ViewProfile
def view_profile(request):    
    """
    This view_profile method is used to retrieve information from database to display
    doctors and patients profile.

    :param request: It's a HttpResponse from user.

    :type request: HttpResponse.

    :return: If a patient is logged in, it returns a HTML page that displays patients profile.
    If a doctor is logged in, it returns a HTML page that displays doctors profile.

    :rtype: HttpResponse.
    """
    idToken = request.session['LoginId']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    patientId = database.child("Users").child("Patient").get()
    patientIdList = []
    for i in patientId.each():
        patientKey = i.key()
        patientIdList.append(patientKey)
    doctorId = database.child("Users").child("Doctor").get()
    doctorIdList = []
    for i in doctorId.each():
        doctorKey = i.key()
        doctorIdList.append(doctorKey)
    for i in doctorIdList: 
        if(i==a):
            doctorFname = database.child("Users").child("Doctor").child(a).child("fname").get().val()     
            doctorLname = database.child("Users").child("Doctor").child(a).child("lname").get().val()      
            doctorAge = database.child("Users").child("Doctor").child(a).child("age").get().val()  
            doctorDob = database.child("Users").child("Doctor").child(a).child("dob").get().val()  
            doctorGender = database.child("Users").child("Doctor").child(a).child("gender").get().val()  
            doctorSpecializedField = database.child("Users").child("Doctor").child(a).child("sfield").get().val()  
            doctorDesignation = database.child("Users").child("Doctor").child(a).child("designation").get().val()  
            doctorWorkingPlace = database.child("Users").child("Doctor").child(a).child("wplace").get().val()  
            doctorWorkingHour1 = database.child("Users").child("Doctor").child(a).child("timeOne").get().val()    
            doctorWorkingHour2 = database.child("Users").child("Doctor").child(a).child("timeTwo").get().val()  
            doctorVisitingFees = database.child("Users").child("Doctor").child(a).child("vfees").get().val()  
            doctorCnumber = database.child("Users").child("Doctor").child(a).child("cnumber").get().val()  
            doctorBgroup = database.child("Users").child("Doctor").child(a).child("bgroup").get().val()  
            doctorEmail = database.child("Users").child("Doctor").child(a).child("email").get().val()  
            return render(request, 'viewProfile/dprofile.html', {'fname':doctorFname, 'lname':doctorLname, 'age':doctorAge, 'dob':doctorDob, 'gender':doctorGender, 'sfield':doctorSpecializedField, 'designation':doctorDesignation, 'wplace':doctorWorkingPlace,'timeOne':doctorWorkingHour1, 'timeTwo':doctorWorkingHour2, 'vfees':doctorVisitingFees, 'cnumber':doctorCnumber, 'bgroup':doctorBgroup,'email':doctorEmail})
    for j in patientIdList:
        if(j==a):
            patientFname = database.child("Users").child("Patient").child(a).child("fname").get().val()
            patientLname = database.child("Users").child("Patient").child(a).child("lname").get().val()
            patientAge = database.child("Users").child("Patient").child(a).child("age").get().val()
            patientDob = database.child("Users").child("Patient").child(a).child("dob").get().val()
            patientGender = database.child("Users").child("Patient").child(a).child("gender").get().val()
            patientOccupation = database.child("Users").child("Patient").child(a).child("occupation").get().val()
            patientCnumber = database.child("Users").child("Patient").child(a).child("cnumber").get().val()
            patientBgroup = database.child("Users").child("Patient").child(a).child("bgroup").get().val()
            patientEmail = database.child("Users").child("Patient").child(a).child("email").get().val()
            return render(request, 'viewProfile/pprofile.html', {'fname':patientFname,'lname':patientLname,'age':patientAge,'dob':patientDob,'gender':patientGender,'occupation':patientOccupation,'cnumber':patientCnumber,'bgroup':patientBgroup,'email':patientEmail})
    return render(request, 'LogInRegister/home.html')

#DeleteProfile
def delete_profile(request):
    """
    This delete_profile method is used to delete the users information from database.

    :param request: It's a HttpResponse from user.

    :type request: HttpResponse.

    :return: If a patient is logged in, it will remove patient's information.
    If a doctor is logged in, it will remove doctor's information.

    :rtype: HttpResponse.
    """
    idToken = request.session['LoginId']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    patientId = database.child("Users").child("Patient").get()
    patientIdList = []
    for i in patientId.each():
        patientKey = i.key()
        patientIdList.append(patientKey)
    doctorId = database.child("Users").child("Doctor").get()
    doctorIdList = []
    for i in doctorId.each():
        doctorKey = i.key()
        doctorIdList.append(doctorKey)
    for i in doctorIdList:
        if(i==a):
            if request.method == 'POST':
                doctorFname = database.child("Users").child("Doctor").child(a).child("fname").get().val()     
                doctorLname = database.child("Users").child("Doctor").child(a).child("lname").get().val()      
                doctorAge = database.child("Users").child("Doctor").child(a).child("age").get().val()  
                doctorDob = database.child("Users").child("Doctor").child(a).child("dob").get().val()  
                doctorGender = database.child("Users").child("Doctor").child(a).child("gender").get().val()  
                doctorSpecializedField = database.child("Users").child("Doctor").child(a).child("sfield").get().val()  
                doctorDesignation = database.child("Users").child("Doctor").child(a).child("designation").get().val()  
                doctorWorkingPlace = database.child("Users").child("Doctor").child(a).child("wplace").get().val()  
                doctorWorkingHour1 = database.child("Users").child("Doctor").child(a).child("timeOne").get().val()    
                doctorWorkingHour2 = database.child("Users").child("Doctor").child(a).child("timeTwo").get().val()  
                doctorVisitingFees = database.child("Users").child("Doctor").child(a).child("vfees").get().val()
                doctorCnumber = database.child("Users").child("Doctor").child(a).child("cnumber").get().val()  
                doctorBgroup = database.child("Users").child("Doctor").child(a).child("bgroup").get().val()  
                doctorEmail = database.child("Users").child("Doctor").child(a).child("email").get().val()  
                database.child("Users").child("Doctor").child(a).remove()
                subject = 'Pashe Achi Account Deletion'
                message = 'Hello {}, Your Pashe Achi account has been deleted.'.format(doctorFname)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [doctorEmail,]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, 'LogInRegister/login.html')
    
    for j in patientIdList:
        if(j==a):
            if request.method == 'POST':
                patientFname = database.child("Users").child("Patient").child(a).child("fname").get().val()
                patientLname = database.child("Users").child("Patient").child(a).child("lname").get().val()
                patientAge = database.child("Users").child("Patient").child(a).child("age").get().val()
                patientDob = database.child("Users").child("Patient").child(a).child("dob").get().val()
                patientGender = database.child("Users").child("Patient").child(a).child("gender").get().val()
                patientOccupation = database.child("Users").child("Patient").child(a).child("occupation").get().val()
                patientCnumber = database.child("Users").child("Patient").child(a).child("cnumber").get().val()
                patientBgroup = database.child("Users").child("Patient").child(a).child("bgroup").get().val()
                patientEmail = database.child("Users").child("Patient").child(a).child("email").get().val()
                database.child("Users").child("Patient").child(a).remove()
                subject = 'Pashe Achi Account Deletion'
                message = 'Hello {}, Your Pashe Achi account has been deleted.'.format(patientFname)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [patientEmail,]
                send_mail(subject, message, email_from, recipient_list)
                return render(request, 'LogInRegister/login.html')
    return render(request, 'viewProfile/profile.html')

