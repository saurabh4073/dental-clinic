
---

# Clinic Management Platform

This platform manages clinics, doctors, patients, and their relationships. It includes user authentication, CRUD operations for clinics, doctors, and patients, and allows the scheduling and tracking of visits. 

## Table of Contents
- [Setup](#setup)
- [Running the Platform](#running-the-platform)
- [Key Features](#key-features)
- [REST API Endpoints](#rest-api-endpoints)
- [Configurations](#configurations)
- [Assumptions](#assumptions)

---

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/saurabh4073/dental-clinic.git
   cd dental-clinic
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Install and configure PostgreSQL.
   - Create a database and user for the application, then set up the environment variables in an `.env` file (use `.env.example` as a template):
     ```plaintext
     DJANGO_SECRET_KEY=your_secret_key
     DATABASE_NAME=your_db_name
     DATABASE_USER=your_db_user
     DATABASE_PASSWORD=your_db_password
     DATABASE_HOST=localhost
     DATABASE_PORT=5432
     ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser for accessing the Django Admin site:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Running the Platform
After setting up, access the platform at [http://localhost:8000](http://localhost:8000). Use the admin panel to add specialties (procedures) and other administrative data.

## Key Features
1. **User Authentication**:
   - Users can log in and out, with role-based access to administrative functions.
  
2. **Clinic Management**:
   - Add, edit, and delete clinic information.
   - View clinic details, including affiliated doctors and patient count.

3. **Doctor Management**:
   - Add, edit, and delete doctors and associate them with specialties.
   - View doctor details, including affiliated clinics, patient count, and work schedules.
   - Support for adding multiple specialties for each doctor.

4. **Patient Management**:
   - Add, edit, and delete patients.
   - Track patients’ past visits and future appointments.

5. **Appointment Scheduling**:
   - Schedule appointments between patients and doctors, with working schedules and available times considered.
   - Display doctor schedules on the calendar with available working days highlighted.

6. **Dynamic Scheduling with Working Schedules**:
   - Automatically update available slots based on doctors' working days and times.
   - Affiliated doctors can be assigned to specific clinics with defined office addresses and schedules.

## REST API Endpoints
### User Authentication
- **Login**: `/api/login/`
  - Method: `POST`
  - Description: Authenticate a user and create a session.

- **Logout**: `/api/logout/`
  - Method: `POST`
  - Description: Terminate the user's session.

### Clinic Endpoints
- **List Clinics**: `/api/clinics/`
  - Method: `GET`
  - Description: Retrieve all clinics.

- **Add Clinic**: `/api/clinics/add/`
  - Method: `POST`
  - Description: Add a new clinic.

- **Clinic Details**: `/api/clinics/<clinic_id>/`
  - Method: `GET`
  - Description: Retrieve details for a specific clinic, including doctors and patients.

- **Edit Clinic**: `/api/clinics/<clinic_id>/edit/`
  - Method: `POST`
  - Description: Update clinic information.

### Doctor Endpoints
- **List Doctors**: `/api/doctors/`
  - Method: `GET`
  - Description: Retrieve all doctors.

- **Add Doctor**: `/api/doctors/add/`
  - Method: `POST`
  - Description: Add a new doctor.

- **Doctor Details**: `/api/doctors/<doctor_id>/`
  - Method: `GET`
  - Description: Retrieve details for a specific doctor, including clinics and specialties.

- **Edit Doctor**: `/api/doctors/<doctor_id>/edit/`
  - Method: `POST`
  - Description: Update doctor information and assign specialties.

### Patient Endpoints
- **List Patients**: `/api/patients/`
  - Method: `GET`
  - Description: Retrieve all patients.

- **Add Patient**: `/api/patients/add/`
  - Method: `POST`
  - Description: Add a new patient.

- **Patient Details**: `/api/patients/<patient_id>/`
  - Method: `GET`
  - Description: Retrieve details for a specific patient, including visits and upcoming appointments.

- **Schedule Visit**: `/api/patients/<patient_id>/visit/`
  - Method: `POST`
  - Description: Schedule a new visit for a patient with a doctor.

### Schedule Management
- **Fetch Available Clinics and Doctors by Specialty**: `/api/specialty/<specialty_id>/doctors-clinics/`
  - Method: `GET`
  - Description: Get a list of doctors and clinics available for a given specialty.

## Configurations
- **Django Admin**: Use Django Admin to manage specialties, users, and other backend data.
- **Environment Variables**: Store sensitive data like `DJANGO_SECRET_KEY` and database credentials in the `.env` file.

## Assumptions
- **Specialty Data**: It is assumed that the specialties (procedures) are added through the Django Admin site.
- **Working Schedule Conflicts**: The platform does not currently prevent conflicts in doctor schedules across clinics.
- **User Roles**: Access control for different user roles is not enforced beyond basic login authentication.

--- 