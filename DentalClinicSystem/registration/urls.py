from . import views
from django.urls import path

app_name = 'registration'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('createPatient', views.RegistrationPatient.as_view(), name='create_patient'),
    path('createDoctor', views.RegistrationDoctor.as_view(), name='create_doctor'),
    path('login', views.Login.as_view(), name = 'login'),
    path('createService', views.RegistrationService.as_view(), name = 'create_service'),
    path('createAppointment',views.RegistrationAppointment.as_view(), name='create_appointment'),
    path('editProfile',views.EditProfile.as_view(), name='edit_profile'),
    path('adminControls',views.MyAdmin.as_view(),name = 'create_admin'),
    path('viewAppointment', views.RegistrationViewAppointment.as_view(), name='view_appointment'),
    path('deleteAppointment/<int:AppointmentID>', views.DeleteAppointment.as_view(), name='delete_appointment'),
    path('updateService',views.UpdateService.as_view(), name='update_service')
    ]

