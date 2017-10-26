from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.
@python_2_unicode_compatible
class Doctor(models.Model):
    def __str__(self):
        return self.firstName + self.lastName
    @staticmethod
    def createDoctor(firstName, lastName, contact, dob, address, user):
        p = Doctor()
        p.firstName = firstName
        p.lastName = lastName
        p.contact = contact
        p.dob = dob
        p.address = address
        p.user = user
        return p

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.ForeignKey(
        'Address',
        on_delete = models.CASCADE,
    )




@python_2_unicode_compatible
class Patient(models.Model):
    def __str__(self):
        return self.firstName + self.lastName
    @staticmethod
    def createPatient(firstName, lastName, contact, dob, address, user, doctor):
        p = Patient()
        p.firstName = firstName
        p.lastName = lastName
        p.contact = contact
        p.dob = dob
        p.address = address
        p.user = user
        return p

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.CASCADE,
        null=True
    )
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.ForeignKey(
        'Address',
        on_delete = models.CASCADE,
    )
@python_2_unicode_compatible
class Address(models.Model):
    def __str__(self):
        return self.city
    @staticmethod
    def create_address(parameters):
        address = Address()
        address.line1 = parameters.get("line1")
        address.line2 = parameters.get("line2")
        address.city = parameters.get("city")
        address.state = parameters.get("state")
        address.pinCode = parameters.get("pinCode")
        address.save()
        return address

    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pinCode = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=10,default = "India")




@python_2_unicode_compatible
class Appointment(models.Model):
    def __str__(self):
        return "Appointement"
    pass
