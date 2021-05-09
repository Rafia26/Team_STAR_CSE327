from django.shortcuts import render, redirect
from makeAppointment.models import Appointment
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timezone
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

def appointment_form(request):
    """
    This method is used to get the values from the appointment form to store data of appointments in the database.
    And it sends the confirmation email of appointment to the doctor and patient.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: This method redirects to another method.

    :rtype: HttpResponse.
    """ 
    import time
    import pytz
    tz = pytz.timezone('Asia/Dhaka')
    timeNow = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(timeNow.timetuple()))
    doctorId = request.POST.get('doctorId')
    date = request.POST.get('date')
    timeSlot = request.POST.get('timeSlot')
    idtoken= request.session['LoginId']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    #a = "6ktQk2bH3ZddF4suT8LRS3xlXJ83"
    data = {
        'date':date,
        'timeSlot':timeSlot,
        'patientId': a,
        'doctorId':doctorId
    }
    doctorFirstName = database.child("Users").child("Doctor").child(doctorId).child("fname").get().val()
    doctorLastName = database.child("Users").child("Doctor").child(doctorId).child("lname").get().val()
    doctorEmail = database.child("Users").child("Patient").child(doctorId).child("email").get().val()
    global patientName
    patientName = database.child("Users").child("Patient").child(a).child("fname").get().val()
    patientEmail = database.child("Users").child("Patient").child(a).child("email").get().val()
    subject = 'Pashe Achi Appointment Confirmation'
    message = 'Hello {}, Your appointment with {} {} is confirmed.'.format(patientName,doctorFirstName,doctorLastName)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [patientEmail,]
    send_mail(subject, message, email_from, recipient_list)
    subject = 'Pashe Achi Appointment Confirmation'
    message = 'Hello {}, {} has added an appointment with you.'.format(doctorFirstName, patientName)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [doctorEmail,]
    send_mail(subject, message, email_from, recipient_list)
    database.child("Appointments").child(millis).set(data)
    return redirect("appointment_form_redirect")

def appointment_form_redirect(request):
    """
    This method renders a HTML file with patient name.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: This method returns a HTML page that displays the appointment confirmation message.

    :rtype: HttpResponse.
    """ 
    return render(request, 'makeAppointment/confirm.html', {'patientName':patientName})
    
def create_appointment(request):
    """
    This method is used to retrieve doctor's name,id,timeslot from database to display in the appointment form.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: This method redirects to another method.

    :rtype: HttpResponse.
    """ 
    docId = database.child("Users").child("Doctor").get()
    docIdList = []
    for i in docId.each():
        docIdKey = i.key()
        docIdList.append(docIdKey)
    doctorNameList = []
    timeOneList = []
    timeTwoList = []
    doctorId = []
    for i in docIdList:
        tempDoctorName = database.child("Users").child("Doctor").child(i).child("fname").get().val()
        doctorNameList.append(tempDoctorName)
        tempTimeOne = database.child("Users").child("Doctor").child(i).child("timeOne").get().val()
        timeOneList.append(tempTimeOne)
        tempTimeTwo = database.child("Users").child("Doctor").child(i).child("timeTwo").get().val()
        timeTwoList.append(tempTimeTwo)
        dId = i
        doctorId.append(dId)
    global allDoctorName, timeSlot
    allDoctorName = zip(doctorNameList,doctorId)
    timeSlot = zip(doctorId,timeOneList,timeTwoList)
    return redirect("create_appointment_redirect")

def create_appointment_redirect(request):
    """
    This method is used to retrieve doctor's name,id,timeslot from database to display in the appointment form.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: This method returns a html page that displays the appointment form.

    :rtype: HttpResponse.
    """
    return render(request, 'makeAppointment/makeAppointment.html',
                {'allDoctorName':allDoctorName,'timeSlot':timeSlot})