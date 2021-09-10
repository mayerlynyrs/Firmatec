"""User model."""

# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#Utilities
from utils.models import BaseModel, Cliente, Planta, Region, Provincia, Ciudad
# from users import User, Sexo, Civil, Nacionalidad, SistemaSalud, SistemaPrevision, Banco, TipoCta
# atributos, cambiar_clave, codigo, email, rut, sexo, estado_civil, fecha_nacimiento, telefono,
# nacionalidad, domicilio, planta, sistema_salud, sistema_prevision, banco, tipo_cta, cuenta


class Sexo(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este sexo, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class Civil(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este estado civil, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class Nacionalidad(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True,
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar esta nacionalidad, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class SistemaSalud(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este Sistema de Salud, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class SistemaPrevision(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este estado Sistema de Prevision, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class Banco(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este banco, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre

class TipoCta(models.Model):
    nombre = models.CharField(
        max_length=120,
        unique=True
    )
    status = models.BooleanField(
        default=True,
        help_text='Para desactivar este tipo de cuenta, deshabilite esta casilla.'
    )
    created_date = models.DateTimeField(
            default=timezone.now,
            null=True,
            blank=True
    )
    
    def __str__(self):
        return self.nombre


class User(BaseModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to rut and add some extra fields.
    """
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    atributos = models.JSONField(blank=True, null=True)

    cambiar_clave = models.BooleanField(
        'Cambiar Clave',
        default=True,
        help_text='Marque esta casilla para que el usuario cambie su clave después de ingresar.'
    )

    codigo = models.CharField(
        'código',
        help_text='Identificador único del sistema de gestión.',
        max_length=6,
        unique=True,
        blank=True,
        null=True
    )

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este email registrado.'
        }
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    planta = models.ManyToManyField(
        Planta,
        help_text='Seleccione solo una planta si el perfil que esta seleccionado es Trabajador.'
    )

    rut_regex = RegexValidator(
        regex=r'^[0-9]{7,9}[0-9kK]{1}$',
        message='El RUT debe ser valido. Ingresalo sin puntos ni guiones.'
    )

    rut = models.CharField(
        max_length=12,
        # validators=[rut_regex, ],
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este RUT registrado.'
        }
    )

    sexo = models.ForeignKey(Sexo, on_delete=models.PROTECT, null=True, blank=True)

    estado_civil = models.ForeignKey(Civil, on_delete=models.PROTECT, null=True, blank=True)

    fecha_nacimiento = models.DateField(null=True, blank=True)

    telefono_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El numero de telefono debe ser ingresado en el siguiente formato +999999999. Solo puede ingresar hasta 15 digitos.'
    )

    telefono = models.CharField(
        'Teléfono',
        validators=[telefono_regex, ],
        max_length=15,
        blank=True,
        null=True
    )

    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.PROTECT, null=True, blank=True)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True)

    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)

    domicilio = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    sistema_salud = models.ForeignKey(SistemaSalud, on_delete=models.PROTECT, null=True, blank=True)

    sistema_prevision = models.ForeignKey(SistemaPrevision, on_delete=models.PROTECT, null=True, blank=True)

    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, null=True, blank=True)

    tipo_cuenta = models.ForeignKey(TipoCta, on_delete=models.PROTECT, null=True, blank=True)

    cuenta = models.CharField(
        'Número de cuenta',
        max_length=30,
        blank=True,
        unique=True,
        null=True
    )

    def __str__(self):
        """Return RUT."""
        return self.rut

    def get_short_name(self):
        """Return RUT."""
        return self.rut
