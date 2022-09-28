from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from schoolapp.models import Programa
from .serializers import ProgramaSerializer

class ProgramaView(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    serializer_class = ProgramaSerializer
    queryset = Programa.objects.all()

