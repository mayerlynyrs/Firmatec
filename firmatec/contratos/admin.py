"""Contratos Admin."""

# Django
from django.contrib import admin
# Models
from contratos.models import Plantilla, Contrato, DocumentosContrato, Tipo


class DocumentoContratoInLine(admin.TabularInline):
    model = DocumentosContrato
    fields = ('archivo',)
    extra = 1

@admin.register(Plantilla)
class PlantillaAdmin(admin.ModelAdmin):
    """PlantillaAdmin model Admin."""

    fields = ('nombre', 'tipo', 'archivo', 'cliente', 'plantas', 'activo')
    list_display = ('codigo', 'nombre', 'tipo', 'cliente', 'plantas_list', 'activo', 'modified_by', )
    # list_display = ('codigo', 'nombre', 'tipo', 'cliente', 'plantas_list', 'activo', 'modified_by', 'modified', )
    list_filter = ['plantas', ]
    search_fields = ('nombre', 'tipo', 'plantas_nombre', )

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.plantas.all())


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    """ContratoAdmin model Admin."""

    fields = ('usuario', 'estado', 'obs', 'archivado')
    list_display = ('usuario', 'plantas_list', 'estado', 'archivado', 'modified', 'created_by')
    #list_filter = ['usuario__planta', ]
    search_fields = ('usuario__rut', 'usuario__last_name', 'usuario__first_name',)

    inlines = [DocumentoContratoInLine]

    def plantas_list(self, obj):
        return u", ".join(o.nombre for o in obj.usuario.planta.all())

@admin.register(DocumentosContrato)
class DocumentoContrato(admin.ModelAdmin):
    """DocumentoContratoAdmnin model Admin."""

    fields = ('contrato', 'archivo', )
    list_display = ('contrato_usuario', 'modified')
    search_fields = ('contrato', )

    def contrato_usuario(self, obj):
        return str(obj.contrato.usuario) + '-' + obj.nombre_archivo


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    fields = ('nombre', )
    list_display = ('nombre', 'created', 'modified',)
