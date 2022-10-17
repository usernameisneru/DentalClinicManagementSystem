import datetime

from django.db import models

# Create your models here.


class Person(models.Model):
    username = models.CharField(max_length=15, primary_key = True)
    password = models.CharField(max_length=15, null=False)
    Person_type = (('P', 'Patient'), ('D', 'Doctor'),('A', 'Admin'))
    Name = models.CharField(max_length=100, null = False)
    Age = models.IntegerField(null= False, default= 1)
    Type = models.CharField(max_length=1, choices=Person_type)


class Doctor(Person):
    Years_of_Experience = models.IntegerField(null= False, default= 1)
    D_type = (('O', 'Orthodontist'), ('P', 'Prosthodontist'), ('E', 'Endodontist'))
    maxPatient = models.IntegerField(default=0)
    Type_of_Doctor = models.CharField(max_length=1, choices=D_type)
    TimeIn = models.TimeField(null = False, default= datetime.datetime.now())
    TimeOut = models.TimeField(null = False, default= datetime.datetime.now())
    def __str__(self):
        return self.username+" "+str(self.Years_of_Experience)


class Patient(Person):
    Address = models.CharField(max_length=50, null= False)
    ContactNum = models.CharField(max_length= 20, null = False)
    def __str__(self):
        return self.username

class Admin(Person):
    ClinicName = models.CharField(max_length=10,null= False, default=0)

class Services(models.Model):
    ServiceId = models.AutoField(primary_key = True)
    ServiceOffered = models.CharField(max_length=50,null = False)
    ServicePrice = models.IntegerField(default = 1,null= False)
    DoctorFK = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    AdminFK = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ServiceId)+" "+self.ServiceOffered+" "+str(self.ServicePrice)




class Receipt(models.Model):
    Receipt_Number = models.AutoField(primary_key = True)
    PaymentTotal = models.IntegerField()


class Payment(models.Model):
    PaymentID = models.AutoField(primary_key = True)
    Payment_method = models.CharField(max_length=20,null= False)
    payment_amount = models.IntegerField(default= 1,null= False)
    payment_Date = models.DateTimeField(null=False)


class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key = True)
    Services_Offered = models.ForeignKey(Services, on_delete = models.CASCADE)
    Appointment_DoctorUsername = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Appointment_PatientUsername = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Appointment_reason = models.CharField(max_length= 100, null = False)
    Appointment_date = models.DateField(null= False)
    Appointment_status =  models.BooleanField(default=False)
    Appointment_time = models.TimeField(null = False, default= datetime.datetime.now())