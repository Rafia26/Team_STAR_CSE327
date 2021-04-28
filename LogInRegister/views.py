from django.shortcuts import render
from LogInRegister.models import LogIn
from LogInRegister.models import SignUp
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

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
storage = firebase.storage()
database = firebase.database()


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
def home(request):
    """
    This home method is used to display the home page 
     with Machine Learning API ChatBot
     and used to login the registered and validate user.
     
     
    :param request: it's a HttpResponse from user.


    :type request: HttpResponse.


    :return: this home method returns a home page
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
            print (j['emailVerified'])

            checkUser = j['emailVerified']

            if checkUser is False:
                    message = "Please check your Email Inbox and Verify your Account"
                    return render(request,"login.html",{"message":message})



        if user is not None:
            print(user['localId'])
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

#Signup
def signup(request):
    """
    This signup method is used to display the signup page.


    :param request: it's a HttpResponse from user.


    :type request: HttpResponse.


    :return: this signup method returns a signup page
     which is a HTML page.


    :rtype: HttpResponse.
    """
    return render(request, 'LogInRegister/signup.html')

#PostSignup    
def post_signup(request):
    """
    This post_signup method is used to registers the user
     and send a verification email to the user.


    :param request: it's a HttpResponse from user.


    :type request: HttpResponse.


    :return: this post_signup method returns a login page 
     after successfull registration.
    else it will return to the signup page
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
        return render(request, 'LogInRegister/signup.html', {"msg2":message2})

    uid = user['localId']

    data = {"fname":userFname, "lname":userLname, 
            "age":userAge, "dob":userDob, 
            "gender":userGender, "occupation":userOccupation, 
            "cnumber":userCnumber, "bgroup":userBgroup, 
            "email":userEmail, "password":userPassword, 
            "cpassword":userCPassword
            }
    database.child("Users_Details").child(uid).set(data)

    return render(request, 'LogInRegister/login.html', {"msg1":message1})

#ForgetPassword    
def forget_password(request):
    """
    This forget_password method is used to recover the 
     forgotten password of a user
     and send a recovery email to the user.


    :param request: it's a HttpResponse from user.


    :type request: HttpResponse.


    :return: this forget_password method returns the login page
     after successfully sending a password recovery email to a user.
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
