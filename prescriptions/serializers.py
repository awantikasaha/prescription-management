from rest_framework import serializers
from .models import Medication, Patient, Prescription


class MedicationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Medication
        fields = ['id', 'name', 'dosage', 'frequency', 'duration_days', 'start_date', 'end_date']


class PrescriptionSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True)
    patientId = serializers.CharField(source='patient.external_id')
    doctorName = serializers.CharField(source='doctor_name')
    active = serializers.SerializerMethodField()
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patientId', 'doctorName', 'notes', 'created_at', 'start_date', 'end_date', 'active', 'medications']

    def get_active(self, obj):
        return obj.active


class CreateMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'frequency', 'duration_days']


class CreatePrescriptionSerializer(serializers.Serializer):
    patientId = serializers.CharField(max_length=64)
    doctorName = serializers.CharField(max_length=255)
    notes = serializers.CharField(required=False, allow_blank=True)
    medications = CreateMedicationSerializer(many=True)

    def validate_medications(self, value):
        if not value:
            raise serializers.ValidationError('At least one medication is required.')
        return value

    def create(self, validated_data):
        patient_id = validated_data['patientId']
        patient, _ = Patient.objects.get_or_create(external_id=patient_id)
        prescription = Prescription.objects.create(
            patient=patient,
            doctor_name=validated_data['doctorName'],
            notes=validated_data.get('notes', ''),
        )
        medications = []
        for med_data in validated_data['medications']:
            medication = Medication(
                prescription=prescription,
                **med_data,
            )
            medication.save()
            medications.append(medication)
        return prescription
