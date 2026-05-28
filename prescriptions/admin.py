from django.contrib import admin
from .models import Medication, Patient, Prescription


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'name']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor_name', 'created_at', 'active']
    readonly_fields = ['active', 'start_date', 'end_date']


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'dosage', 'frequency', 'duration_days', 'prescription']
