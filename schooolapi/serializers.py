from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from schoolapp.models import Programa

class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'