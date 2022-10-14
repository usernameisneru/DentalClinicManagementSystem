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

    def __str__(self):
        return self.username+" "+str(self.Years_of_Experience)


class Patient(Person):
    Address = models.CharField(max_length=50, null= False)
    ContactNum = models.CharField(max_length= 20, null = False)


class Services(models.Model):
    ServiceId = models.AutoField(primary_key = True)
    ServiceOffered = models.CharField(max_length=50,null = False)
    ServicePrice = models.IntegerField(default = 1,null= False)

    def __str__(self):
        return str(self.ServiceId)+" "+self.ServiceOffered+" "+str(self.ServicePrice)

class Admin(Person):
    Salary = models.IntegerField(null= False, default=0)


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