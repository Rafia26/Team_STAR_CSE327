from django.db import models

# Create your models here.


class Donation(models.Model):
    
    """
        This Donation class is extended from the model class. 
        So, it has all the functionality of the model class.

        Attributes: name, contactNum, email, amount, trxId.

        Functions: This class requires no functions.

        This class is used to create objects for database entry of donation.
    """
    donorName = models.CharField(max_length=100)
    contactNum = models.CharField(max_length=14)
    email = models.EmailField(max_length=50)
    amount = models.IntegerField()
    trxId = models.CharField(max_length=10)
    
    
    

