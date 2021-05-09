from django.shortcuts import render, redirect
from LogInRegister.models import LogIn
from LogInRegister.models import PatientSignUp
from LogInRegister.models import DoctorSignUp
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

#Login
def login(request):
    """
    This login method is used to display the login page. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this login method returns a login page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/login.html')

#Home
def home(request):
    """
    This home method is used to display the home page. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this home method returns a home page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/home.html')

#GoogleLogin
def google_login(request):
    """
    This google_login method is used to login the user using Google Signin API.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this google_login method returns the home page
    which is a HTML page.
    else it will return to the log in page.

    :rtype: HttpResponse.
    """
    if request.method == 'POST':
        userEmail = request.POST['email']
        userPhoto = request.POST['photo']
        uid = request.POST['uid']
        userName = request.POST['username']   
        data = {
                'username':userName,'uid':uid,
                'email':userEmail, 'Image_Url':userPhoto
        }
        database.child('Google_User_Details').child(uid).set(data)
        request.session['uid'] = str(uid)
        request.session['localId'] = uid
        return render(request,'LogInRegister/home.html')
    else:
        return render(request,'LogInRegister/login.html')

#Home
def post_login(request):
    """
    This post_login method is used to display the home page with Machine Learning API ChatBot
    and used to login the registered and validate user.
     
    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this post_login method returns a home page
    which is a HTML page.
    else it will return to the log in page.

    :rtype: HttpResponse.
    """
    userEmail = request.POST.get('email')
    userPassword = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(userEmail,userPassword)
        new = authe.get_account_info(user['idToken'])
        for j in new['users']:
            #print (j['emailVerified'])
            checkUser = j['emailVerified']
            if checkUser is False:
                    message = "Please check your Email Inbox and Verify your Account"
                    return render(request,"login.html",{"message":message})
        if user is not None:
            #print(user['localId'])
            sessionId = user['localId']
            request.session['LoginId'] = str(sessionId)
            request.session['localId'] = sessionId       
    except:
        message0 = "Account not registered or verified!"
        return render(request, 'LogInRegister/login.html', {"msg0":message0})
    sessionId = user['idToken'] 
    request.session['LoginId'] = str(sessionId)
    uid = user['localId']
    data = {"email":userEmail, "password":userPassword}
    database.child("Login_Details").child("User_Details").child(uid).set(data) 
    return render(request, 'LogInRegister/home.html')
    #return redirect("login_test")

#LoginTest
def login_test(request):
    """
    This login_test method is used to test post_login funtion
    I've used this for testing purpose
    My post_login function redirects here. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this login method returns a home page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/home.html')

#PatientSignup
def patient_signup(request):
    """
    This patient_signup method is used to display the signup page for the patient.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this patient_signup method returns a signup page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/patient_signup.html')

#DoctorSignup
def doctor_signup(request):
    """
    This doctor_signup method is used to display the signup page for the patient.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this doctor_signup method returns a signup page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/doctor_signup.html')


#PatientPostSignup    
def patient_post_signup(request):
    """
    This patient_post_signup method is used to registers the user
    and send a verification email to the user.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this patient_post_signup method returns a login page after successfull registration.
    else it will return to the patient_signup page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    userFname = request.POST.get('fname')
    userLname = request.POST.get('lname')
    userAge = request.POST.get('age')
    userDob = request.POST.get('dob')
    userGender = request.POST.get('gender')
    userOccupation = request.POST.get('occupation')
    userCnumber = request.POST.get('cnumber')
    userBgroup = request.POST.get('bgroup')
    userEmail = request.POST.get('email')
    userPassword = request.POST.get('password')
    userCPassword = request.POST.get('cpassword')
    try:
        user = authe.create_user_with_email_and_password(userEmail,userPassword)
        authe.send_email_verification(user['idToken'])
        message1 = "A verification link has been sent to your account. Confirm to proceed!"   
    except:
        message2 = "Unable to create account. Please try again!"
        return render(request, 'LogInRegister/patient_signup.html', {"msg2":message2})
        #return redirect("psignup_test")
    uid = user['localId']
    data = {"fname":userFname, "lname":userLname, 
            "age":userAge, "dob":userDob, 
            "gender":userGender, "occupation":userOccupation, 
            "cnumber":userCnumber, "bgroup":userBgroup, 
            "email":userEmail, "password":userPassword, 
            "cpassword":userCPassword
    }
    database.child("Users").child("Patient").child(uid).set(data)
    return render(request, 'LogInRegister/login.html', {"msg1":message1})
    #return redirect("psignup_test")

#PatientSignUpTest
def psignup_test(request):
    """
    This psignup_test method is used to test patient_post_signup function
    I've used this for testing purpose
    My patient_post_signup function redirects here. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this login method returns a login page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/login.html', {"msg1":message1})

#DoctorPostSignup    
def doctor_post_signup(request):
    """
    This doctor_post_signup method is used to registers the user
    and send a verification email to the user.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this doctor_post_signup method returns a login page after successfull registration.
    else it will return to the doctor_signup page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    userFname = request.POST.get('fname')
    userLname = request.POST.get('lname')
    userAge = request.POST.get('age')
    userDob = request.POST.get('dob')
    userGender = request.POST.get('gender')
    userSpecializedField = request.POST.get('sfield')
    userDesignation = request.POST.get('designation')
    userWorkingPlace = request.POST.get('wplace')
    userWorkingHour1 =  request.POST.get('timeOne')
    userWorkingHour2 =  request.POST.get('timeTwo')
    userVisitingFees = request.POST.get('vfees')
    userCnumber = request.POST.get('cnumber')
    userBgroup = request.POST.get('bgroup')
    userEmail = request.POST.get('email')
    userPassword = request.POST.get('password')
    userCPassword = request.POST.get('cpassword')
    try:
        user = authe.create_user_with_email_and_password(userEmail,userPassword)
        authe.send_email_verification(user['idToken'])
        message1 = "A verification link has been sent to your account. Confirm to proceed!" 
    except:
        message2 = "Unable to create account. Please try again!"
        return render(request, 'LogInRegister/doctor_signup.html', {"msg2":message2})
        #return redirect("dsignup_test")
    uid = user['localId']
    data = {"fname":userFname, "lname":userLname, 
            "age":userAge, "dob":userDob, 
            "gender":userGender, "sfield":userSpecializedField, 
            "designation":userDesignation, "wplace":userWorkingPlace,
            "timeOne":userWorkingHour1, "timeTwo":userWorkingHour2,
            "vfees":userVisitingFees,"cnumber":userCnumber, 
            "bgroup":userBgroup, "email":userEmail,
            "password":userPassword,"cpassword":userCPassword
    }
    database.child("Users").child("Doctor").child(uid).set(data)
    data2 = {"fname":userFname, "lname":userLname, 
            "age":userAge, "dob":userDob, 
            "gender":userGender, "sfield":userSpecializedField, 
            "designation":userDesignation, "wplace":userWorkingPlace,
            "timeOne":userWorkingHour1, "timeTwo":userWorkingHour2,
            "vfees":userVisitingFees,"cnumber":userCnumber, 
            "bgroup":userBgroup, "email":userEmail,
            "password":userPassword,"cpassword":userCPassword
    }
    database.child("Specialties").child(userSpecializedField).child(uid).set(data2)
    return render(request, 'LogInRegister/login.html', {"msg1":message1})
    #return redirect("dsignup_test")

#DoctorSignUpTest
def dsignup_test(request):
    """
    This dsignup_test method is used to test post_doctor_signup function
    I've used this for testing purpose
    My doctor_post_signup function redirects here. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this login method returns a login page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/login.html', {"msg1":message1})

#ForgetPassword    
def forget_password(request):
    """
    This forget_password method is used to recover the forgotten password of a user
    and send a recovery email to the user.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this forget_password method returns the login page after successfully sending a password recovery email to a user.
    else it will return to the forgetpassword page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    if request.method == 'POST':
        userEmail = request.POST['email']
        authe.send_password_reset_email(userEmail)
        message3 = "Email has been sent for password RESET. Please check your inbox"
        return render(request,'LogInRegister/login.html',{"msg3":message3})
    else:
        return render(request,'LogInRegister/forgetpassword.html')

#Logout
def logout(request):
    """
    This logout method is used to logout the user.

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this logout method returns the login page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    try: 
        del request.session['uid']
        del request.session['localId']
        auth.logout(request)
    except:
        pass
    return render(request,'LogInRegister/login.html')

#AboutUs
def about_us(request):
    """
    This about_us method is used to display the about page. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this about_us method returns a about page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/about_us.html')

#ContactUs
def contact_us(request):
    """
    This contact_us method is used to display the contact page. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this contact_us method returns a contact page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/contact_us.html')

#Description
def description(request):
    """
    This description method is used to display the contact page. 

    :param request: it's a HttpResponse from user.

    :type request: HttpResponse.

    :return: this description method returns a description page
    which is a HTML page.

    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/description.html')

