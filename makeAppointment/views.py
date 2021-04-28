from django.shortcuts import render
from makeAppointment.models import Appointment
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

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
storage = firebase.storage()
database = firebase.database()

def appointment_form(request):
    
   """
    This method is used to get the values from the appointment from and stores the data of appointments
    in the database.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this method returns a html page that displays the appointment confirmation message.

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

   idtoken= request.session['uid']
   a = authe.get_account_info(idtoken)
   a = a['users']
   a = a[0]
   a = a['localId']

   data = {
      'Date':date,
      'Time_Slot':timeSlot,
      'Patient_ID': a,
      'Doctor_ID':doctorId
   }

   patientName = database.child("Users").child("Patient").child(a).child("name").get().val()
   database.child("Appointments").child(millis).set(data)
   return render(request, 'makeAppointment/confirm.html', {'patientName':patientName})

def create_appointment(request):

   """
    This method is used to retrieve doctor's name,id,timeslot from database to display in the appointment form.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this method returns a html page that displays the appointment form.

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
      tempDoctorName = database.child("Users").child("Doctor").child(i).child('name').get().val()
      doctorNameList.append(tempDoctorName)
      tempTimeOne = database.child("Users").child("Doctor").child(i).child('time_one').get().val()
      timeOneList.append(tempTimeOne)
      tempTimeTwo = database.child("Users").child("Doctor").child(i).child('time_two').get().val()
      timeTwoList.append(tempTimeTwo)
      dId = i
      doctorId.append(dId)
      
   allDoctorName = zip(doctorNameList,doctorId)
   timeSlot = zip(doctorId,timeOneList,timeTwoList)

   return render(request, 'makeAppointment/makeAppointment.html',{'allDoctorName':allDoctorName,'timeSlot':timeSlot})