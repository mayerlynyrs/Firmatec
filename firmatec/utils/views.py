from django.shortcuts import render

# Create your views here.
"""Utils Views. """

from django.db.models import Count
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Count
# Modelo
from utils.models import Planta
from ficheros.models import Fichero
from contratos.models import Contrato
from users.models import User


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # Obtengo las plantas del Usuario
        plantas = self.request.user.planta.all()
        # Obtengo los ficheros de las plantas a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            plantas__in=plantas, activo=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT']).exists():
            context['contratos'] = Contrato.objects.filter(
                usuario=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                usuario__planta__in=plantas, estado=Contrato.POR_FIRMAR)

        return context


class Inicio(LoginRequiredMixin, TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        # Obtengo los datos del Usuario
        context['dusuario'] = User.objects.filter()
        # Obtengo las plantas del Usuario
        plantas = self.request.user.planta.all()
        # Obtengo los ficheros de las plantas a las que pertenece el usuario
        context['ficheros'] = Fichero.objects.filter(
            plantas__in=plantas, activo=True
        ).distinct()
        # Obtengo los contratos del usuario si no es administrador.
        if not self.request.user.groups.filter(name__in=['Administrador']).exists():
            context['contratos'] = Contrato.objects.filter(
                usuario=self.request.user).order_by('modified')
        else:
            # Obtengo todos los contratos por firmar de todas las plantas a las
            # que pertenece el usuario.
            context['contratos'] = Contrato.objects.filter(
                usuario__planta__in=plantas, estado=Contrato.POR_FIRMAR)
            context['result'] = Contrato.objects.values(
                'created_by_id').order_by('usuario__planta').annotate(count=Count('usuario__planta'))

        return context

    # template_name = 'inicio.html'

    # def get_context_data(self, **kwargs):
    #     context = super(Inicio, self).get_context_data(**kwargs)
    #     # Obtengo las plantas del Usuario
    #     plantas = self.request.user.planta.all()
    #     # Obtengo los ficheros de las plantas a las que pertenece el usuario
    #     context['ficheros'] = Fichero.objects.filter(
    #         plantas__in=plantas, activo=True
    #     ).distinct()
    #     # Obtengo los usuarios con el perfil Administrador Contratos
    #     context['administradorc'] = User.objects.filter(groups='3')
    #     # Conteo 
    #     planta = Planta.objects.filter(nombre__contains='Planta 2')
    #     context['firmartrab'] = Contrato.objects.filter(usuario__planta__in=planta).count()
    #     #result = Contrato.objects.values('created_by_id').order_by('created_by_id').annotate(count=Count('created_by_id'))
    #     cuenta_plantas = Contrato.objects.values('usuario__planta').order_by('usuario__planta').annotate(count=Count('usuario__planta'))
    #     #context['result'] = Contrato.objects.values('created_by_id').order_by('usuario__planta').annotate(count=Count('usuario__planta'))
    #     # context['result'] = len(Contrato.objects.filter(created_by_id='3', usuario__planta__in='2'))
    #     # context['firmartrab'] = Contrato.objects.count()
    #     # context['firmartrab'] = Contrato.objects.filter(
    #     #         usuario__planta__in=plantas).count()
    #     # context['firmartrab'] = Contrato.objects.filter(publisher__name='BaloneyPress').count()
    #     # Obtengo los contratos del usuario si no es administrador.
    #     if not self.request.user.groups.filter(name__in=['Administrador']).exists():
    #         context['contratos'] = Contrato.objects.filter(
    #             usuario=self.request.user).order_by('created_by')
    #     else:
    #         # Obtengo todos los contratos por firmar de todas las plantas a las
    #         # que pertenece el usuario.
    #         context['contratos'] = Contrato.objects.filter(
    #             usuario__planta__in=plantas, estado=Contrato.POR_FIRMAR)
    #         context['result'] = Contrato.objects.filter(
    #             usuario__planta=plantas).values('created_by_id').order_by('usuario__planta').annotate(count=Count('usuario__planta'))
    

    #     return context