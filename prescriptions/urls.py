from django.urls import path
from .views import PatientPrescriptionListView, PrescriptionCreateView

urlpatterns = [
    path('prescriptions', PrescriptionCreateView.as_view(), name='create-prescription'),
    path('patients/<str:patient_id>/prescriptions', PatientPrescriptionListView.as_view(), name='patient-prescriptions'),
]
