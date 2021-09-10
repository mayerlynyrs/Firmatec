from django.contrib import admin

# Register your models here.
"""Utils Admin."""

# Django
# django-import-export
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from utils.models import Cliente, Planta, Region, Provincia, Ciudad


class ClienteSetResource(resources.ModelResource):

    class Meta:
        model = Cliente
        fields = ('id', 'codigo', 'nombre', )


class PlantaSetResource(resources.ModelResource):
    cliente = fields.Field(column_name='cliente', attribute='cliente', widget=ForeignKeyWidget(Cliente, 'nombre'))

    class Meta:
        model = Planta
        fields = ('id', 'codigo', 'nombre', 'cliente')


class RegionSetResource(resources.ModelResource):

    class Meta:
        model = Region
        fields = ('id', 'nombre', 'status', )


class ProvinciaSetResource(resources.ModelResource):
    region = fields.Field(column_name='region', attribute='region', widget=ForeignKeyWidget(Region, 'nombre'))

    class Meta:
        model = Provincia
        fields = ('id', 'nombre', 'region', 'status', )


class CiudadSetResource(resources.ModelResource):
    provincia = fields.Field(column_name='provincia', attribute='provincia', widget=ForeignKeyWidget(Provincia, 'nombre'))

    class Meta:
        model = Ciudad
        fields = ('id', 'nombre', 'provincia', 'status', )


@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ClienteAdmin model admin."""

    resource_class = ClienteSetResource
    fields = ('codigo', 'nombre', )
    list_display = ('id', 'codigo', 'nombre',)
    search_fields = ['nombre', ]


@admin.register(Planta)
class PlantaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """PlantaAdmin model admin."""

    resource_class = PlantaSetResource
    fields = ('codigo', 'cliente', 'nombre', )
    list_display = ('id', 'codigo', 'nombre', 'cliente')
    list_filter = ['cliente', ]
    search_fields = ('codigo', 'nombre', 'cliente__nombre')


@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """RegionAdmin model admin."""

    resource_class = RegionSetResource
    fields = ('nombre', )
    list_display = ('id', 'nombre',)
    search_fields = ['nombre', ]


@admin.register(Provincia)
class ProvinciaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """ProvinciaAdmin model admin."""

    resource_class = ProvinciaSetResource
    fields = ('region', 'nombre', )
    list_display = ('id', 'nombre', 'region',)
    list_filter = ['region', ]
    search_fields = ('nombre', 'region__nombre')


@admin.register(Ciudad)
class CiudadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """CiudadAdmin model admin."""

    resource_class = CiudadSetResource
    fields = ('provincia', 'nombre', )
    list_display = ('id', 'nombre', 'provincia',)
    list_filter = ['provincia', ]
    search_fields = ('nombre', 'provincia__nombre')

# admin.site.register(Region)
