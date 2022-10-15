from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Patient, Doctor, Services, Appointment, Person, Admin


class PatientForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.TextInput)
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


class DoctorForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.TextInput)
    Name = forms.CharField(widget=forms.TextInput)
    Age = forms.CharField(widget=forms.NumberInput)
    Type = 'D'
    Years_of_Experience = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = Doctor
        fields = ['username', 'password', 'Name', 'Age', 'Years_of_Experience']

    def __init__(self,*args,**kwargs):
        super(DoctorForm, self).__init__(*args,*kwargs)
        self.instance.Type = self.Type


class AdminForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.TextInput)
    Name = forms.CharField(widget=forms.TextInput)
    Age = forms.CharField(widget=forms.NumberInput)
    Type = 'A'
    Salary = forms.CharField(widget=forms.NumberInput)
    
    class Meta:
        model = Admin
        fields = ['username', 'password', 'Name', 'Age','Salary']

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

    class Meta:
        model = Appointment
        fields = ['Appointment_DoctorUsername','Services_Offered','Appointment_reason', 'Appointment_date']