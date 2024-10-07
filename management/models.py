from django.db import models
from django.contrib.auth.models import User

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    email = models.EmailField()

class Doctor(models.Model):
    NPI = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    specialties = models.ManyToManyField(Specialty)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    last_4_digits_ssn = models.CharField(max_length=4)
    gender = models.CharField(max_length=10)
    affiliated_doctors = models.ManyToManyField(Doctor, through='Visit')

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    procedures_done = models.CharField(max_length=200)
    visit_date = models.DateTimeField()
    doctor_notes = models.TextField()
    booking_date = models.DateField(null=True)


class WorkingSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='working_schedules')
    working_day = models.CharField(max_length=10)  
    start_time = models.TimeField()
    end_time = models.TimeField()
    office_address = models.TextField(null=True)  
    affiliated_clinics = models.ManyToManyField(Clinic)
    def __str__(self):
        return f"{self.doctor.name} - {self.working_day}: {self.start_time} to {self.end_time}"