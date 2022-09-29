from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('registrar/', register, name='registrar-usuario'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('listar/programa/', listar_programa),
    path('crear/programa/', crear_programa),
    path('actualizar/programa/<int:id>', actualizar_programa, name='actualizar-programa'),
    path('listar/estudiantes', listar_estudiante, name='listar-estudiantes'),
    path('crear/estudiante', crear_estudiante, name='crear-estudiantes'),
    path('actualizar/estudiante/<int:id>', actualizar_estudiante, name='actualizar-estudiante'),
    path('eliminar/estudiante/<int:id>', eliminar_estudiante, name='eliminar-estudiante'),
    path('listar/profesor/', listar_profesor, name='listar-profesor'),
    path('crear/profesor/', crear_profesor, name='crear-profesor')
]
