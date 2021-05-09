from django.shortcuts import render
from makeAppointment.models import Appointment
from django.conf import settings
from django.core.mail import send_mail
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

"""
Global Variables
"""
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
storage = firebase.storage()
database = firebase.database()

def appointments(request):
    """
    This method is used to retrieve appointments details from database to display
    doctors and patients upcoming appointments.

    :param request: It's a HttpResponse from user.

    :type request: HttpResponse.

    :return: If the database doesn't contain any appointments, it returns a HTML page showing text.
             Else,
                If a patient is logged in, it returns a HTML page that displays patients upcoming appointments.
                If a doctor is logged in, it returns a HTML page that displays doctors upcoming appointments.
                If the logged in user has no appointments, it returns a HTML page showing text.
                
    :rtype: HttpResponse.
    """
    idtoken = request.session['LoginId']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timeStamp = database.child("Appointments").get()
    if timeStamp is None:
        return render(request, 'viewAppointment/noAppointment.html')
    else:
        timeStampList = []
        for i in timeStamp.each():
            timeStampKey = i.key()
            timeStampList.append(timeStampKey)
        doctorNameList = []
        addressList = []
        appointmentDateList = []
        appointmentTimeList = []
        patientNameList = []
        patientAgeList = []
        row = []
        rowNo = 0      
        patientIdView = None
        doctorIdView = None
        for i in timeStampList:           
            patientId = database.child("Appointments").child(i).child("patientId").get().val()
            doctorId = database.child("Appointments").child(i).child("doctorId").get().val()  
            if (patientId == a):
                patientIdView = database.child("Appointments").child(i).child("patientId").get().val()
                rowNo = rowNo+1
                row.append(rowNo)
                tempDate = database.child("Appointments").child(i).child("date").get().val()
                appointmentDateList.append(tempDate)
                tempTime = database.child("Appointments").child(i).child("timeSlot").get().val()
                appointmentTimeList.append(tempTime)
                tempDoctorName = database.child("Users").child("Doctor").child(doctorId).child("fname").get().val()
                doctorNameList.append(tempDoctorName)            
                tempAddress = database.child("Users").child("Doctor").child(doctorId).child("wplace").get().val()
                addressList.append(tempAddress)
            elif(doctorId == a):
                doctorIdView = database.child("Appointments").child(i).child("doctorId").get().val()
                rowNo = rowNo+1
                row.append(rowNo)
                tempDate = database.child("Appointments").child(i).child("date").get().val()
                appointmentDateList.append(tempDate)
                tempTime = database.child("Appointments").child(i).child("timeSlot").get().val()
                appointmentTimeList.append(tempTime)
                tempPatientName = database.child("Users").child("Patient").child(patientId).child("fname").get().val()
                patientNameList.append(tempPatientName)
                tempPatientAge = database.child("Users").child("Patient").child(patientId).child("age").get().val()
                patientAgeList.append(tempPatientAge)
        appointmentDetails = zip(row,timeStampList,addressList,doctorNameList,appointmentDateList,appointmentTimeList)
        appointmentDetailsDoctor = zip(row,timeStampList,patientNameList,patientAgeList,appointmentDateList,appointmentTimeList)       
        if (patientIdView == a):
            patientName = database.child("Users").child("Patient").child(a).child("fname").get().val()
            return render(request, 'viewAppointment/viewAppointment.html',
                        {'appointmentDetails':appointmentDetails,
                        'patientName':patientName,'timeStampList':timeStampList})              
        elif(doctorIdView == a):
            doctorName = database.child("Users").child("Doctor").child(a).child("fname").get().val()
            return render(request, 'viewAppointment/doctorView.html',
                        {'appointmentDetailsDoctor':appointmentDetailsDoctor,
                        'doctorName':doctorName, 'timeStampList':timeStampList})   
        else:
            return render(request, 'viewAppointment/noAppointment.html')      

def cancel_appointment(request,timeStampList):
    """
    This method is used to cancel appointments and send email after cancellation.

    :param request: It's a HttpResponse from user.
    :param timeStampList: It's the appointment id clicked by user to cancel appointment.

    :type request: HttpResponse.
    :type timeStampList: Integer.

    :return: It returns the HTML page of homepage.

    :rtype: HttpResponse.
    """
    patientId = database.child("Appointments").child(timeStampList).child("patientId").get().val()
    doctorId = database.child("Appointments").child(timeStampList).child("doctorId").get().val()
    idtoken = request.session['LoginId']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    appointmentDate = database.child("Appointments").child(timeStampList).child("date").get().val()
    appointmentTime = database.child("Appointments").child(timeStampList).child("timeSlot").get().val()
    doctorName = database.child("Users").child("Doctor").child(doctorId).child("fname").get().val()
    patientName = database.child("Users").child("Patient").child(patientId).child("fname").get().val()
    doctorEmail = database.child("Users").child("Doctor").child(doctorId).child("email").get().val()
    patientEmail = database.child("Users").child("Patient").child(patientId).child("email").get().val()
    if request.method == 'POST':
        database.child("Appointments").child(timeStampList).remove()
    if (patientId == a):
        subject = 'Pashe Achi Appointment Cancellation'
        message = 'Hello {}, Your appointment on {} at {} with {} has been cancelled.'.format(doctorName,appointmentDate,appointmentTime,patientName)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [doctorEmail,]
        send_mail(subject, message, email_from, recipient_list)
    elif(doctorId == a):
        subject = 'Pashe Achi Appointment Cancellation'
        message = 'Hello {}, Your appointment on {} at {} with {} has been cancelled.'.format(patientName,appointmentDate,appointmentTime,doctorName)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [patientEmail,]
        send_mail(subject, message, email_from, recipient_list)
    return render(request, 'LogInRegister/home.html')