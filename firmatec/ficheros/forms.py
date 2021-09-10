"""Fichero Forms"""

# Django
from django import forms
from django.contrib.auth.models import Group
# Firmatec Model
from utils.models import Planta
from ficheros.models import Fichero


class FicheroCreateForm(forms.ModelForm):
    nombre = forms.CharField(required=True, label="Nombre",
                                 widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    desc = forms.CharField(required=True, label="Descripción",
                                widget=forms.Textarea(attrs={'class': "form-control-lg"}))

    plantas = forms.ModelMultipleChoiceField(queryset=Planta.objects.none(), required=True, label="Planta",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(FicheroCreateForm, self).__init__(*args, **kwargs)
        if not user.groups.filter(name='Administrador').exists():
            self.fields['plantas'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['plantas'].queryset = Planta.objects.all()

    class Meta:
        model = Fichero
        fields = ("nombre", "desc", "archivo", "plantas", "activo", )

