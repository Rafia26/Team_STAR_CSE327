from django.db import models


# Create your models here.
class LogIn(models.Model):
    """
    This LogIn class is extended from the Model class 
    so it has all the functionality of the model class.

    Attributes: userEmail, userPassword.

    Functions: This LogIn class requires no functions.

    This LogIn class used to create objects for database entry.
    """
    userEmail = models.EmailField(max_length=50)
    userPassword = models.CharField(max_length=50)


class PatientSignUp(models.Model):
    """
    This PatientSignUp class is extended from the Model class 
    so it has all the functionality of the model class.

    Attributes: userFname, userLname, userAge, userDob,  
    userGender, userOccupation, userCnumber, userBgroup, 
    userEmail, userPassword, userCPassword.

    Functions: This SignUp class requires no functions.

    This PatientSignUp class used to create objects for database entry.
    """
    userFname = models.CharField(max_length=50)
    userLname = models.CharField(max_length=50)
    userAge = models.IntegerField()
    userDob = models.DateField(auto_now=False, auto_now_add=False)
    userGender = models.CharField(max_length=10)
    userOccupation = models.CharField(max_length=30)
    userCnumber = models.CharField(max_length=30)
    userBgroup = models.CharField(max_length=20)
    userEmail = models.EmailField(max_length=50)
    userPassword = models.CharField(max_length=50)
    userCPassword = models.CharField(max_length=50)


class DoctorSignUp(models.Model):
    """
    This DoctorSignUp class is extended from the Model class 
    so it has all the functionality of the model class.

    Attributes: userFname, userLname, userAge, userDob,  
    userGender, userSpecializedField, userDesignation,  userWorkingPlace,
    userWorkingHour1, userWorkingHour2, userVisitingFees, userCnumber, userBgroup, userEmail, userPassword, userCPassword.

    Functions: This DoctorSignUp class requires no functions.

    This DoctorSignUp class used to create objects for database entry.
    """
    userFname = models.CharField(max_length=50)
    userLname = models.CharField(max_length=50)
    userAge = models.IntegerField()
    userDob = models.DateField(auto_now=False, auto_now_add=False)
    userGender = models.CharField(max_length=10)
    userSpecializedField = models.CharField(max_length=30)
    userDesignation = models.CharField(max_length=30)
    userWorkingPlace = models.CharField(max_length=30)
    userWorkingHour1 =  models.TimeField(auto_now=False, auto_now_add=False)
    userWorkingHour2 =  models.TimeField(auto_now=False, auto_now_add=False)
    userVisitingFees = models.DecimalField(max_digits=10, decimal_places=2)
    userCnumber = models.CharField(max_length=30)
    userBgroup = models.CharField(max_length=20)
    userEmail = models.EmailField(max_length=50)
    userPassword = models.CharField(max_length=50)
    userCPassword = models.CharField(max_length=50)






    
