"""Utils Admin."""

# Django
from django.contrib import admin
# django-import-export
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin
#Models
from ficheros.models import Fichero
# Utils Model
from utils.models import Planta


class FicheroSetResource(resources.ModelResource):
    plantas = fields.Field(
        column_name='plantas',
        attribute='plantas',
        widget=ManyToManyWidget(Planta, ',', 'pk'))


    class Meta:
        model = Fichero
        fields = ('id', 'nombre', 'desc', 'plantas')


@admin.register(Fichero)
class FicheroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """FicheroAdmin model Admin"""

    resource_class = FicheroSetResource
    fields = ('nombre', 'desc', 'archivo', 'plantas', 'activo', )
    list_display = ('id', 'nombre', 'plantas_list', 'modified_by', 'modified')
    list_filter = ['plantas', ]
    search_fields = ('nombre', 'planta__nombre')

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.plantas.all())
