from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Patient, Doctor, Services, Appointment, Person, Admin


class PatientForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    Name = forms.CharField(widget=forms.TextInput)
    Age = forms.CharField(widget=forms.NumberInput)
    Type = 'P'
    Address = forms.CharField(widget=forms.TextInput)
    ContactNum = forms.CharField(widget=forms.NumberInput)

    class Meta:
        model = Patient
        fields = ['username', 'password', 'Name', 'Age', 'Address', 'ContactNum']

    def __init__(self,*args,**kwargs):
        super(PatientForm, self).__init__(*args,**kwargs)
        self.instance.Type = self.Type
        self.fields['ContactNum'].required = False

    def clean_Age(self):
        age = self.data.get('Age')
        if int(age) < 18:
            raise ValidationError("Age should not be less than 18")
        else:
            return age

class DoctorForm(ModelForm):
    D_type = (('O', 'Orthodontist'), ('P', 'Prosthodontist'), ('E', 'Endodontist'))
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    Name = forms.CharField(widget=forms.TextInput)
    Age = forms.CharField(widget=forms.NumberInput)
    Type = 'D'
    Years_of_Experience = forms.IntegerField(widget=forms.NumberInput)
    Type_of_Doctor = forms.ChoiceField(choices= D_type)
    maxPatient = forms.IntegerField(widget= forms.NumberInput)
    TimeIn = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    TimeOut = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))


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
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.TextInput)
    Name = forms.CharField(widget=forms.TextInput)
    Age = forms.CharField(widget=forms.NumberInput)
    Type = 'A'
    Clinic = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Admin
        fields = ['username', 'password', 'Name', 'Age','Clinic']

    def __init__(self,*args,**kwargs):
        super(AdminForm, self).__init__(*args,*kwargs)
        self.instance.Type = self.Type



class ServiceForm(ModelForm):
    DoctorFK = forms.ModelChoiceField(widget=forms.Select(), queryset=Doctor.objects.all())
    ServiceOffered = forms.CharField(widget=forms.TextInput)
    ServicePrice = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = Services
        fields = ['DoctorFK','ServiceOffered', 'ServicePrice']



class AppointmentForm(ModelForm):
    Appointment_DoctorUsername = forms.ModelChoiceField(widget=forms.Select(),queryset=Doctor.objects.all())
    Services_Offered = forms.ModelChoiceField(widget=forms.Select(),queryset=Services.objects.all())
    Appointment_reason = forms.CharField(widget=forms.TextInput)
    Appointment_date = forms.DateField(widget=forms.DateInput)
    status = False

    def __init__(self, *args, **kwargs):  # constructor
        super(AppointmentForm,self).__init__(*args, **kwargs)
        self.instance.status = self.status
        '''dc = Doctor.objects.only('username')
        service = Services.objects.filter()'''

    class Meta:
        model = Appointment
        fields = ['Appointment_DoctorUsername','Services_Offered','Appointment_reason', 'Appointment_date']