from rest_framework import serializers
from .models import *


class UploadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ["uploaded_at", "id", "file_hash", "file_size", "original_filename"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "title", "subject", "level"]


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ["id", "objective", "explanation", "qcm"]


class QCMSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCM
        fields = "__all__"

