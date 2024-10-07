from django.test import TestCase
from django.urls import reverse
from .models import Clinic, Doctor, Patient, Specialty, WorkingSchedule, Visit
from django.utils import timezone

class ClinicTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            phone_number='1234567890',
            city='Test City',
            state='Test State',
            email='clinic@test.com'
        )

    def test_clinic_creation(self):
        self.assertEqual(self.clinic.name, 'Test Clinic')
        self.assertEqual(self.clinic.city, 'Test City')

    def test_clinics_list_view(self):
        response = self.client.get(reverse('clinics_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Clinic')

    def test_clinic_detail_view(self):
        response = self.client.get(reverse('clinic_detail', args=[self.clinic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Clinic')


class DoctorTests(TestCase):
    def setUp(self):
        self.specialty = Specialty.objects.create(name='General Practice')
        self.doctor = Doctor.objects.create(
            NPI='12345',
            name='Test Doctor',
            email='doctor@test.com',
            phone_number='9876543210'
        )
        self.doctor.specialties.add(self.specialty)

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.name, 'Test Doctor')
        self.assertIn(self.specialty, self.doctor.specialties.all())

    def test_doctors_list_view(self):
        response = self.client.get(reverse('doctors_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Doctor')

    def test_doctor_detail_view(self):
        response = self.client.get(reverse('doctor_detail', args=[self.doctor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Doctor')


class PatientTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            name='Test Patient',
            address='123 Test St',
            phone_number='1112223333',
            date_of_birth='1990-01-01',
            last_4_digits_ssn='1234',
            gender='M'
        )

    def test_patient_creation(self):
        self.assertEqual(self.patient.name, 'Test Patient')

    def test_patients_list_view(self):
        response = self.client.get(reverse('patients_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Patient')

    def test_patient_detail_view(self):
        response = self.client.get(reverse('patient_detail', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Patient')


class VisitTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name='Test Clinic', phone_number='1234567890', city='Test City', state='Test State', email='clinic@test.com')
        self.specialty = Specialty.objects.create(name='General Practice')
        self.doctor = Doctor.objects.create(NPI='12345', name='Test Doctor', email='doctor@test.com', phone_number='9876543210')
        self.patient = Patient.objects.create(name='Test Patient', address='123 Test St', phone_number='1112223333', date_of_birth='1990-01-01', last_4_digits_ssn='1234', gender='M')
        
        # Use timezone.now() for dates
        self.visit = Visit.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            clinic=self.clinic,
            procedures_done=self.specialty.name,
            visit_date=timezone.now(),
            booking_date=timezone.now()
        )

    def test_visit_creation(self):
        self.assertEqual(self.visit.patient.name, 'Test Patient')
        self.assertEqual(self.visit.doctor.name, 'Test Doctor')
        self.assertEqual(self.visit.clinic.name, 'Test Clinic')

    def test_visit_view(self):
        response = self.client.get(reverse('patient_detail', args=[self.patient.id]))
        self.assertContains(response, 'Test Patient')
        self.assertContains(response, 'Test Doctor')


class WorkingScheduleTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name='Test Clinic', phone_number='1234567890', city='Test City', state='Test State', email='clinic@test.com')
        self.specialty = Specialty.objects.create(name='General Practice')
        self.doctor = Doctor.objects.create(NPI='12345', name='Test Doctor', email='doctor@test.com', phone_number='9876543210')
        self.working_schedule = WorkingSchedule.objects.create(doctor=self.doctor, working_day='Monday', start_time='09:00', end_time='17:00')
        self.working_schedule.affiliated_clinics.add(self.clinic)

    def test_working_schedule_creation(self):
        self.assertEqual(self.working_schedule.doctor.name, 'Test Doctor')
        self.assertIn(self.clinic, self.working_schedule.affiliated_clinics.all())

