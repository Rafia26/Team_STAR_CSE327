from django.db import models


class Ratings(models.Model):
    """
        This class is extended from the model class. So, it has all the functionality of model class.

        This class is used to create objects from database entry.
    """

    doctorId = models.CharField(max_length=100)
    patientId = models.CharField(max_length=100)
    serviceR = models.TimeField(auto_now=False, auto_now_add=False)
    behaviourR = models.TimeField(auto_now=False, auto_now_add=False)
    accdR = models.TimeField(auto_now=False, auto_now_add=False)
