from django.db import models
from cgi import maxlen
from unittest.util import _MAX_LENGTH

# Create your models here.

class Licor(models.Model):
    id = models.AutoField(primary_key=True)
    codigoReferencia = models.TextField(blank=True,null=True)
    titulo = models.TextField(blank=True,null=True)
    descripcion = models.TextField(blank=True,null=True)
    precio = models.FloatField(blank=True,null=True)
    origen = models.TextField(blank=True,null=True)
    cantidad = models.TextField(blank=True,null=True) #Volumen o peso
    graduacion = models.FloatField(blank=True,null=True)
    urlProducto = models.URLField(unique=True)
    urlImagen = models.URLField(blank=True,null=True)
    enStock = models.BooleanField()
   
class Categoria(models.Model):
    nombre = models.TextField(unique=True)
    licor = models.ManyToManyField(Licor, blank=True)
    
