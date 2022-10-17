from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import request

from .models import Patient, Doctor, Services, Appointment, Person, Admin


class PatientForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput,label='Input Username')
    password = forms.CharField(widget=forms.PasswordInput,label='Input Username')
    Name = forms.CharField(widget=forms.TextInput,label='Input Name')
    Age = forms.CharField(widget=forms.NumberInput,label='Input Age')
    Type = 'P'
    Address = forms.CharField(widget=forms.TextInput,label='Input Address')
    ContactNum = forms.CharField(widget=forms.NumberInput,label='Input Contact Number')

    class Meta:
        model = Patient
        fields = ['username', 'password', 'Name', 'Age', 'Address', 'ContactNum']

    def __init__(self,*args,**kwargs):
        super(PatientForm, self).__init__(*args,**kwargs)
        self.instance.Type = self.Type
        self.fields['ContactNum'].required = False

    def clean_Age(self):
        age = self.data.get('Age')
        if int(age) < 0:
            raise ValidationError("Age should not be less than 0")
        else:
            return age

class DoctorForm(ModelForm):
    D_type = (('O', 'Orthodontist'), ('P', 'Prosthodontist'), ('E', 'Endodontist'))
    username = forms.CharField(widget=forms.TextInput,label='Input Username')
    password = forms.CharField(widget=forms.PasswordInput,label='Input Password')
    Name = forms.CharField(widget=forms.TextInput,label='Input Name')
    Age = forms.CharField(widget=forms.NumberInput,label='Input Age')
    Type = 'D'
    Years_of_Experience = forms.IntegerField(widget=forms.NumberInput,label='Input Years of Experience')
    Type_of_Doctor = forms.ChoiceField(choices= D_type,label='Choose Type of Doctor')
    maxPatient = forms.IntegerField(widget= forms.NumberInput,label='Input Number of Max Patient')
    TimeIn = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),label='Input Time In')
    TimeOut = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),label='Input Time Out')


    class Meta:
        model = Doctor
        fields = ['username', 'password', 'Name', 'Age', 'Years_of_Experience','Type_of_Doctor','maxPatient','TimeIn','TimeOut']

    def __init__(self,*args,**kwargs):
        super(DoctorForm, self).__init__(*args,**kwargs)
        self.instance.Type = self.Type


    def clean_Age(self):
        age = self.data.get('Age')
        if int(age) < 18:
            raise ValidationError("Age should not be less than 18")
        else:
            return age
    def clean_Years_of_Experience(self):
        yrs = self.data.get('Years_of_Experience')
        if int(yrs) < 0:
            raise ValidationError("Years of Experience should not be less than 0")
        else:
            return yrs
    def clean_maxPatient(self):
        max = self.data.get('maxPatient')
        if int(max) < 0:
            raise ValidationError("Number of Patients must not be less than 0")
        else:
            return max

class AdminForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput,label='Input Username')
    password = forms.CharField(widget=forms.PasswordInput,label='Input Password')
    Name = forms.CharField(widget=forms.TextInput,label='Input Name')
    Age = forms.CharField(widget=forms.NumberInput,label='Input Age')
    Type = 'A'
    Clinic = forms.CharField(widget=forms.TextInput,label='Input Clinic Name')

    class Meta:
        model = Admin
        fields = ['username', 'password', 'Name', 'Age','Clinic']

    def __init__(self,*args,**kwargs):
        super(AdminForm, self).__init__(*args,*kwargs)
        self.instance.Type = self.Type

    def clean_Age(self):
        age = self.data.get('Age')
        if int(age) < 18:
            raise ValidationError("Age should not be less than 18")
        else:
            return age
class ServiceForm(ModelForm):
    DoctorFK = forms.ModelChoiceField(widget=forms.Select(), queryset=Doctor.objects.all(),label='Choose Doctor')
    ServiceOffered = forms.CharField(widget=forms.TextInput,label='Name of Service')
    ServicePrice = forms.IntegerField(widget=forms.NumberInput,label='Service Price')

    class Meta:
        model = Services
        fields = ['DoctorFK','ServiceOffered', 'ServicePrice']


class AppointmentForm(ModelForm):
    Appointment_DoctorUsername = forms.ModelChoiceField(widget=forms.Select(),queryset=Doctor.objects.all(),label='Choose Doctor')
    Services_Offered = forms.ModelChoiceField(widget=forms.Select(),queryset=Services.objects.all(),label='Choose Service Offered')
    Appointment_reason = forms.CharField(widget=forms.TextInput,label='Input Appointment Reason')
    Appointment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}), label='Appointment_Date')
    status = False


    class Meta:
        model = Appointment
        fields = ['Appointment_DoctorUsername','Services_Offered','Appointment_reason', 'Appointment_date']

    def __init__(self, did,*args, **kwargs):  # constructor
        super(AppointmentForm, self).__init__(*args, **kwargs)
        doctor = Doctor.objects.filter(person_ptr_id = did)
        service = Services.objects.filter(DoctorFK_id=did)
        self.fields['Appointment_DoctorUsername'].queryset = doctor
        self.fields['Services_Offered'].queryset = service
        self.instance.status = self.status

    def clean_Appointment_date(self):
        Appointment_date = self.cleaned_data['Appointment_date']
        print(Appointment_date > date.today())
        if Appointment_date <= date.today():
            raise ValidationError("The date entered should not be before today!")
        elif Appointment_date > (date.today()+timedelta(30)):
            raise ValidationError("The date entered should not be more than a month from now!")
        else:
            return Appointment_date

class pickDoctor(forms.Form):
    doc = forms.ModelChoiceField(widget=forms.Select(), queryset=Doctor.objects.all(),label='Choose Doctor')