"""Users Forms"""

# Django
from django import forms
from django.forms import inlineformset_factory, RadioSelect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import TextInput
from django.contrib.auth.models import Group
# Firmatec Model
from utils.models import Cliente, Planta, Region, Provincia, Ciudad
from users.models import Civil, SistemaSalud, SistemaPrevision, TipoCta

User = get_user_model()


class CrearUsuarioForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control-lg"}))
    first_name = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    last_name = forms.CharField(required=True, label="Apellidos",
                                widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    fecha_nacimiento = forms.DateField(required=True, input_formats=["%d/%m/%Y"], label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA','class': "form-control-lg",}))
    estado_civil = forms.ModelChoiceField(queryset=Civil.objects.all(), required=True, label="Estado Civil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    sistema_salud = forms.ModelChoiceField(queryset=SistemaSalud.objects.all(), required=True, label="Sistema Salud",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    sistema_prevision = forms.ModelChoiceField(queryset=SistemaPrevision.objects.all(), required=True, label="Sistema Prevision",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    tipo_cuenta = forms.ModelChoiceField(queryset=TipoCta.objects.all(), required=True, label="Tipo Cuenta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cuenta = forms.CharField(required=True, label="Número de Cuenta",
                                widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    group = forms.ModelChoiceField(queryset=Group.objects.none(), required=True, label="Perfil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    clientes = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    plantas = forms.ModelMultipleChoiceField(queryset=Planta.objects.none(), required=True, label="Planta",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control-lg",
                          'onkeypress': "return isNumber(event)",
                          'oninput': "checkRut(this)",
                          'title': "El RUT debe ser ingresado sin puntos ni guiones.",
                          'placeholder': '987654321',}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)
        if not user.groups.filter(name='Administrador').exists():
            self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
            self.fields['clientes'].queryset = Cliente.objects.filter(id__in=user.planta.all())
            self.fields['plantas'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['group'].queryset = Group.objects.all()
            self.fields['clientes'].queryset = Cliente.objects.all()
            self.fields['plantas'].queryset = Planta.objects.select_related('cliente')

    class Meta:
        model = User
        fields = ("group", "rut", "first_name", "last_name", "sexo", "email", "telefono", "estado_civil", "fecha_nacimiento", 
                  "nacionalidad", "region", "provincia", "ciudad", "domicilio", "sistema_salud", "sistema_prevision",
                  "banco", "tipo_cuenta", "cuenta", "clientes", "plantas", "is_active", )
        exclude = ('password1', 'password2')



class EditarUsuarioForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control-lg"}))
    first_name = forms.CharField(required=True, label="Nombres",
                                 widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    last_name = forms.CharField(required=True, label="Apellidos",
                                widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    fecha_nacimiento = forms.DateField(required=True, input_formats=["%d-%m-%Y"], label="Fecha de Nacimiento",
                                widget=forms.TextInput(attrs={'placeholder': 'DD-MM-AAAA','class': "form-control-lg"}))
    estado_civil = forms.ModelChoiceField(queryset=Civil.objects.all(), required=True, label="Estado Civil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    sistema_salud = forms.ModelChoiceField(queryset=SistemaSalud.objects.all(), required=True, label="Sistema Salud",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    sistema_prevision = forms.ModelChoiceField(queryset=SistemaPrevision.objects.all(), required=True, label="Sistema Prevision",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    tipo_cuenta = forms.ModelChoiceField(queryset=TipoCta.objects.all(), required=True, label="Tipo Cuenta",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cuenta = forms.CharField(required=True, label="Número de Cuenta",
                                widget=forms.TextInput(attrs={'class': "form-control-lg"}))
    group = forms.ModelChoiceField(queryset=Group.objects.none(), required=True, label="Perfil",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none(), required=True, label="Cliente",
                                   widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control-lg',
                                                              'data-size': '5',
                                                              'data-live-search': 'true',
                                                              'data-live-search-normalize': 'true'
                                                              })
                                   )
    planta = forms.ModelMultipleChoiceField(queryset=Planta.objects.none(), required=True, label="Planta",
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'selectpicker show-tick form-control-lg',
                                                       'data-size': '5',
                                                       'data-live-search': 'true',
                                                       'data-live-search-normalize': 'true'
                                                       })
                                            )
    rut = forms.CharField(required=True, label="RUT",
                          widget=forms.TextInput(attrs={'class': "form-control-lg"}))

        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)

        self.fields['provincia'].queryset = Provincia.objects.none()

        

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['provincia'].queryset = Provincia.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Provincia queryset
        elif self.instance.pk:
            self.fields['provincia'].queryset = self.instance.region.provincia_set.order_by('nombre')

        self.fields['ciudad'].queryset = Provincia.objects.none()
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Provincia queryset
        elif self.instance.pk:
            # self.fields['ciudad'].queryset = self.instance.region.provincia.ciudad_set.order_by('nombre')
            self.fields['ciudad'].queryset = self.instance.provincia.ciudad_set.order_by('nombre')
        if not user.groups.filter(name='Administrador').exists():
            self.fields['group'].queryset = Group.objects.exclude(name__in=['Administrador', 'Administrador Contratos', 'Fiscalizador Interno', 'Fiscalizador DT', ])
            self.fields['cliente'].queryset = Cliente.objects.filter(id__in=user.planta.all())
            self.fields['planta'].queryset = Planta.objects.filter(id__in=user.planta.all())
        else:
            self.fields['group'].queryset = Group.objects.all()
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['planta'].queryset = Planta.objects.none()

        

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['planta'].queryset = Planta.objects.filter(cliente_id=cliente_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty planta queryset
        elif self.instance.pk:
            self.fields['planta'].queryset = self.instance.cliente.planta_set.order_by('nombre')

 
    class Meta:
        model = User
        fields = ("group", "rut", "first_name", "last_name", "sexo", "email", "telefono", "estado_civil", "fecha_nacimiento", 
                  "nacionalidad", "region", "provincia", "ciudad", "domicilio", "sistema_salud", "sistema_prevision",
                  "banco", "tipo_cuenta", "cuenta", "cliente", "planta", "is_active", )
        widgets = {
            'telefono': TextInput(attrs={
                'class': "form-control-lg",
                'type': "number",
                'placeholder': '56912345678'
                }),
            'cuenta': TextInput(attrs={
                'class': "form-control-lg",
                'type': "number"
                }),
        }
