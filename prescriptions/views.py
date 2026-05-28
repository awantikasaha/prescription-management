from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient, Prescription
from .serializers import CreatePrescriptionSerializer, PrescriptionSerializer


class PrescriptionCreateView(APIView):
    def post(self, request):
        serializer = CreatePrescriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save()
        output = PrescriptionSerializer(prescription)
        return Response(output.data, status=status.HTTP_201_CREATED)


class PatientPrescriptionListView(APIView):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, external_id=patient_id)
        prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
        output = PrescriptionSerializer(prescriptions, many=True)
        return Response({'patientId': patient_id, 'prescriptions': output.data})
