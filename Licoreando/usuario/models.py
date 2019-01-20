from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Usuario(AbstractUser, PermissionsMixin):
    username = models.TextField(unique=True)
    email = models.EmailField(blank = True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default = False)
    #USERNAME_FIELD = 'email'
    
class Formulario(models.Model):
    usuario = models.OneToOneField(Usuario, blank = False, null = False, on_delete= models.CASCADE)
    comentario = models.TextField(blank = True, null = True)
    precioMinimo = models.FloatField(blank = True, null = True)
    precioMaximo = models.FloatField(blank = True, null = True)
    graduacionMinima = models.FloatField(blank = True, null = True)
    graduacionMaxima = models.FloatField(blank = True, null = True)
    
class PuntuacionCategoriaLicor(models.Model):
    licor = models.TextField()
    puntuacion = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)
    
class PuntuacionOrigenLicor(models.Model):
    origen = models.TextField()
    puntuacion = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)

class PuntuacionMarcaLicor(models.Model):
    marca =models.TextField()
    puntuacion = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(10)])
    formulario = models.ForeignKey(Formulario,blank = False, null = False, on_delete = models.CASCADE)