from datetime import timedelta
from django.db import models
from django.utils import timezone


class Patient(models.Model):
    external_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Patient {self.external_id}"


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, related_name='prescriptions', on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    @property
    def active(self):
        now = timezone.localtime(timezone.now()).date()
        return self.medications.filter(end_date__gte=now).exists()

    @property
    def start_date(self):
        return self.created_at.date()

    @property
    def end_date(self):
        end_dates = self.medications.values_list('end_date', flat=True)
        return max(end_dates) if end_dates else self.start_date

    def __str__(self):
        return f"Prescription {self.id} for {self.patient.external_id}"


class Medication(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='medications', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=128)
    frequency = models.CharField(max_length=128)
    duration_days = models.PositiveIntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.prescription_id and self.prescription.created_at:
            self.start_date = self.prescription.created_at.date()
            self.end_date = self.start_date + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.dosage})"
