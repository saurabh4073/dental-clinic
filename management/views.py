from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Clinic, Doctor, Patient, Specialty, WorkingSchedule, Visit
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html') 

def logout_view(request):
    logout(request)
    return redirect('login')

def clinics_list(request):
    clinics = Clinic.objects.all()
    clinic_details = []

    for clinic in clinics:
        doctor_count = WorkingSchedule.objects.filter(affiliated_clinics=clinic).values('doctor').distinct().count()
        
        patient_count = Visit.objects.filter(clinic=clinic).values('patient').distinct().count()
        
        clinic_details.append({
            'clinic': clinic,
            'doctor_count': doctor_count,
            'patient_count': patient_count
        })

    return render(request, 'clinics_list.html', {'clinic_details': clinic_details})





def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    affiliated_schedules = WorkingSchedule.objects.filter(affiliated_clinics=clinic).select_related('doctor')
    affiliated_doctors = set(schedule.doctor for schedule in affiliated_schedules)
    
    all_doctors = Doctor.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit_clinic':
            print("Clinic",request.POST)
            clinic.name = request.POST.get('name')
            clinic.city = request.POST.get('city')
            clinic.state = request.POST.get('state')
            clinic.phone_number = request.POST.get('phone_number')
            clinic.email = request.POST.get('email')
            clinic.save()

        elif action == 'add_doctor':
            new_doctor_id = request.POST.get('new_doctor_id')
            office_address = request.POST.get('office_address')
            working_day = request.POST.get('working_day')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            
            if new_doctor_id and office_address and working_day and start_time and end_time:
                new_doctor = get_object_or_404(Doctor, id=new_doctor_id)
                
                working_schedule = WorkingSchedule.objects.create(
                    doctor=new_doctor,
                    working_day=working_day,
                    start_time=start_time,
                    end_time=end_time,
                    office_address=office_address
                )
                
                working_schedule.affiliated_clinics.add(clinic)
                
            return redirect('clinic_detail', clinic_id=clinic.id)

        elif action == 'remove_doctor':
            doctor_id = request.POST.get('doctor_id')
            doctor = get_object_or_404(Doctor, id=doctor_id)
            
            WorkingSchedule.objects.filter(doctor=doctor, affiliated_clinics=clinic).delete()
            
            return redirect('clinic_detail', clinic_id=clinic.id)

    return render(request, 'clinic_detail.html', {
        'clinic': clinic,
        'affiliated_schedules': affiliated_schedules,
        'all_doctors': all_doctors
    })



def add_clinic(request):
    if request.method == 'POST':
        clinic_name = request.POST.get('name')
        clinic_phone = request.POST.get('phone_number')
        clinic_city = request.POST.get('city')
        clinic_state = request.POST.get('state')
        clinic_email = request.POST.get('email')

        clinic = Clinic(
            name=clinic_name,
            phone_number=clinic_phone,
            city=clinic_city,
            state=clinic_state,
            email=clinic_email
        )
        
        clinic.save()
        
        return redirect('clinics_list')
    
    return render(request, 'add_clinic.html')

def add_doctor(request, doctor_id=None):
    if request.method == 'POST':
        npi = request.POST.get('npi')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        specialty_id = request.POST.get('specialties')  

        print("request.POST", request.POST)
        
        doctor = Doctor(
            NPI=npi,
            name=name,
            email=email,
            phone_number=phone_number
        )
        doctor.save()  

        specialty = get_object_or_404(Specialty, id=specialty_id)
        doctor.specialties.add(specialty)  

        return redirect('doctor_detail', doctor_id=doctor.id) 

    specialties = Specialty.objects.all()

    
    context = {
        'specialties': specialties,
    }

    return render(request, 'add_doctor.html', context)


def doctors_list(request):
    doctors = Doctor.objects.all()
    doctor_details = []

    for doctor in doctors:
        clinic_count = doctor.working_schedules.values_list('affiliated_clinics', flat=True).distinct().count()
        
        patient_count = Visit.objects.filter(doctor=doctor).values('patient').distinct().count()
        
        doctor_details.append({
            'doctor': doctor,
            'clinic_count': clinic_count,
            'patient_count': patient_count
        })

    return render(request, 'doctors_list.html', {'doctor_details': doctor_details})




def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    specialties = Specialty.objects.all()
    
    
    affiliated_clinics = Clinic.objects.filter(workingschedule__doctor=doctor).distinct()
    patients = Patient.objects.filter(visit__doctor=doctor).distinct()

    if request.method == 'POST':
        
        doctor.NPI = request.POST.get('npi')
        doctor.name = request.POST.get('name')
        doctor.email = request.POST.get('email')
        doctor.phone_number = request.POST.get('phone_number')
        doctor.save()
        
        if request.POST.get('specialties'):
            doctor.specialties.set([request.POST.get('specialties')])

        return redirect('doctor_detail', doctor_id=doctor.id)

    
    return render(request, 'doctor_detail.html', {
        'doctor': doctor, 
        'specialties': specialties, 
        'affiliated_clinics': affiliated_clinics,
        'patients': patients
    })


def patients_list(request):
    current_time = timezone.now()
    patients = Patient.objects.all()

    patient_details = []

    for patient in patients:
        
        visits = Visit.objects.filter(patient=patient)

        
        last_visit = visits.filter(visit_date__lt=current_time).order_by('-visit_date').first()

        
        next_appointment = visits.filter(visit_date__gte=current_time).order_by('visit_date').first()

        patient_details.append({
            'patient': patient,
            'last_visit_date': last_visit.visit_date if last_visit else None,
            'last_visit_doctor': last_visit.doctor.name if last_visit else None,
            'last_visit_procedure': last_visit.procedures_done if last_visit else None,
            'next_appointment_date': next_appointment.visit_date if next_appointment else None,
            'next_appointment_doctor': next_appointment.doctor.name if next_appointment else None,
            'next_appointment_procedure': next_appointment.procedures_done if next_appointment else None,
        })

    return render(request, 'patients_list.html', {
        'patient_details': patient_details,
    })

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    specialties = Specialty.objects.all()
    
   
    visits = Visit.objects.filter(patient=patient)

    
    current_time = timezone.now()
    past_visits = visits.filter(visit_date__lt=current_time)
    future_appointments = visits.filter(visit_date__gte=current_time)

    if request.method == 'POST':
        
        specialty_id = request.POST.get('specialty')
        clinic_id = request.POST.get('clinic')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        if specialty_id and clinic_id and doctor_id and date and time:
            specialty = get_object_or_404(Specialty, id=specialty_id)
            clinic = get_object_or_404(Clinic, id=clinic_id)
            doctor = get_object_or_404(Doctor, id=doctor_id)
            appointment_datetime = f"{date} {time}"
            try:
                
                appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")
 
                Visit.objects.create(
                    patient=patient,
                    doctor=doctor,
                    clinic=clinic,
                    procedures_done=specialty.name,
                    visit_date=appointment_datetime,
                    doctor_notes="",
                    booking_date=current_time.date()
                )
            except ValueError as e:
                
                print("Error parsing date/time:", e)
    
    return render(request, 'patient_detail.html', {
        'patient': patient,
        'specialties': specialties,
        'visits': past_visits,
        'next_appointments': future_appointments,
    })


def add_patient(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        last_4_digits_ssn = request.POST.get('last_4_digits_ssn')
        gender = request.POST.get('gender')

        
        patient = Patient(
            name=name,
            address=address,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            last_4_digits_ssn=last_4_digits_ssn,
            gender=gender
        )
        patient.save()  

        return redirect('patients_list')

    return render(request, 'add_patient.html')


def fetch_clinics_doctors(request, specialty_id):
 
    working_schedules = WorkingSchedule.objects.filter(
        doctor__specialties__id=specialty_id
    ).select_related('doctor').prefetch_related('affiliated_clinics')

    data = {}
    for schedule in working_schedules:
        doctor_id = schedule.doctor.id
        if doctor_id not in data:
            data[doctor_id] = {
                'doctor': {'id': doctor_id, 'name': schedule.doctor.name},
                'clinics': [],
                'schedules': []
            }
        for clinic in schedule.affiliated_clinics.all():
            if clinic.id not in [c['id'] for c in data[doctor_id]['clinics']]:
                data[doctor_id]['clinics'].append({
                    'id': clinic.id,
                    'name': clinic.name
                })
        data[doctor_id]['schedules'].append({
            'working_day': schedule.working_day,
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M')
        })
        print(data)

    return JsonResponse({'doctors': list(data.values())})