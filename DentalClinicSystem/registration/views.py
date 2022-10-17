from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.db import connection

from .forms import PatientForm, DoctorForm, ServiceForm, AppointmentForm, AdminForm
from .models import Person, Patient, Doctor, Admin, Appointment, Services


# Create your views here.

class HomeView(View):
    template = 'index.html'

    def get(self, request):
        if(request.session['type']=='D'):
            cursorDoctor = connection.cursor()
            cursorDoctor.callproc('dbdentalclinicsystem.appointmentdoctor', [request.session['username']])
            allDoctor = cursorDoctor.fetchall()
            cursorDoctor.close()
            return render(request, self.template, {'allDoctor': allDoctor})
        elif(request.session['type']=='P'):
            cursorSchedule = connection.cursor()
            cursorSchedule.callproc('dbdentalclinicsystem.appointmentschedule', [request.session['username']])
            allSchedule = cursorSchedule.fetchall()
            cursorSchedule.close()
            return render(request, self.template, {'allSchedule': allSchedule})
        elif (request.session['type'] == 'A'):
            cursorService = connection.cursor()
            cursorService.callproc('dbdentalclinicsystem.ServiceEdit')
            doctAssign = cursorService.fetchall()
            cursorService.close()
            return render(request, self.template, {'doctAssign': doctAssign})
        else:
            return render(request, self.template)

class RegistrationPatient(View):
    template = 'createPatient.html'

    def get(self, request):
        form = PatientForm()

        return render(request, self.template,{'form':form})

    def post(self,request):
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('registration:login'))
        return render(request,self.template,{'form':form})


class RegistrationDoctor(View):
    template = 'createDoctor.html'

    def get(self,request):
        form = DoctorForm()
        return render(request, self.template,{'form':form})

    def post(self,request):
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('registration:login'))
        return render(request, self.template, {'form': form})

class MyAdmin(View):
       template = 'adminControls.html'

       def get(self, request):
           form = AdminForm()
           return render(request, self.template, {'form': form})

       def post(self, request):
           form = AdminForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect(reverse('registration:login'))
           return render(request, self.template, {'form': form})


class Login(View):
    template = 'login.html'

    def get(self,request):
        return render(request, self.template)

    def post(self,request):
        uname = request.POST['username']
        pwd = request.POST['password']

        try:
            if Person.objects.get(pk=uname):
                person = Person.objects.get(pk=uname)
                if person.password == pwd:
                    request.session['username'] = person.username
                    request.session['type'] = person.Type
            return redirect(reverse('registration:index'))
        except Person.DoesNotExist:
            user = None


class RegistrationService(View):
    template = 'Service.html'
    def get(self,request):
        form = ServiceForm()
        return render(request, self.template,{'form':form})

    def post(self, request):
        form = ServiceForm(request.POST)
        if form.is_valid():
            admin = Admin.objects.get(pk=request.session['username'])
            Service= form.save(commit=False)
            Service.AdminFK = admin
            Service.save()
            return redirect(reverse('registration:index'))

        return render(request, self.template, {'form': form})

class RegistrationViewAppointment(View):
    template = "AppointmentList.html"

    def get(self, request):
        cursorAppointment = connection.cursor()
        cursorAppointment.callproc('dbdentalclinicsystem.appointmentlist',[request.session['username']])
        allAppointments = cursorAppointment.fetchall()
        cursorAppointment.close()
        return render(request, self.template, {'allAppointments':allAppointments})


class RegistrationAppointment(View):
    template = "createAppointment.html"

    def get(self,request):
        form = AppointmentForm()
        return render(request, self.template,{'form':form})

    def post(self,request):

        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor= Doctor.objects.get(pk = request.session['username'])
            appointment = form.save(commit=False)
            appointment.Appointment_DoctorUsername = doctor
            appointment.save()

            return redirect(reverse('registration:index'))

        return render(request, self.template, {'form': form})


class EditProfile(View):
    template = "editProfile.html"

    def get(self,request):

        if request.session['type'] == 'D':
            doctor = Doctor.objects.get(pk=request.session['username'])
            form = DoctorForm(instance=doctor)
        else:
            patient = Patient.objects.get(pk=request.session['username'])
            form = PatientForm(instance=patient)
        return render(request, self.template,{'form': form})

    def post(self,request):
        if request.session['type'] == 'D':
            doctor = Doctor.objects.get(pk=request.session['username'])
            form = DoctorForm(request.POST, instance=doctor)
        else:
            patient = Patient.objects.get(pk=request.session['username'])
            form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect(reverse('registration:index'))
        return render(request, self.template, {'form': form})

class DeleteAppointment(View):
    template = 'index.html'

    def get(self,request, AppointmentID):
            appointment = Appointment.objects.get(pk=int(AppointmentID))
            appointment.delete()
            return render(request,self.template)