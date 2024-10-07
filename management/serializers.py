from rest_framework import serializers
from .models import Clinic, Doctor, Patient

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['name', 'phone_number', 'city', 'state', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['NPI', 'name', 'specialties', 'email', 'phone_number']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'address', 'phone_number', 'gender']
