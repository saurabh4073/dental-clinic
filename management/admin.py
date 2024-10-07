from django.contrib import admin
from .models import Clinic, Doctor, Patient, Visit, Specialty
# Register your models here.
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Specialty)