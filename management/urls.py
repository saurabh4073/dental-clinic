from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('home/', views.home, name='home'),  
    path('logout/', views.logout_view, name='logout'),  
    path('clinics/add/', views.add_clinic, name='add_clinic'),
    path('clinics/', views.clinics_list, name='clinics_list'),
    path('clinics/<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('patient/add/', views.add_patient, name='add_patient'),
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('fetch_clinics_doctors/<int:specialty_id>/', views.fetch_clinics_doctors, name='fetch_clinics_doctors'),
]
