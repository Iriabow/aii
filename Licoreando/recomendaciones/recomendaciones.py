'''
Created on 23 ene. 2019

@author: viento
'''
import django
from recomendaciones.distancia import getPuntuacionFrase, getPuntuacionRango,\
    getPuntuacionAtributo
django.setup()

from licor.models  import Licor, Categoria
from django.contrib.auth.models import User
from usuario.models import Formulario, PuntuacionCategoriaLicor, PuntuacionMarcaLicor, PuntuacionOrigenLicor


def generaRecomendaciones(idFormulario):
    form = Formulario.objects.filter(pk = idFormulario).first()
    if form:
        recomendaciones={}
        for licor in Licor.objects.all():
            recomendaciones.update(getPuntuacionLicor(form, licor))
            
        veinteMejores = sorted(recomendaciones.items(), key=lambda p: p[1],reverse=True)[0,19]
        
    else:
        return 0
    
    return 1

def getPuntuacionLicor(form,licor):
    puntuacion = 0.0
    puntuacion=puntuacion+getPuntuacionFrase(form.comentario,licor.descripcion)
    puntuacion=puntuacion+getPuntuacionRango(licor.precio,form.precioMinimo,form.precioMaximo)
    puntuacion=puntuacion+getPuntuacionRango(licor.graduacion,form.graduacionMinima,form.graduacionMaxima)
    
    for categoriaF in form.puntuacionCategoriaLicor_set.all():
        for categoriaL in licor.categoria_set.all():
            puntuacion=puntuacion+getPuntuacionAtributo(categoriaF.licor, categoriaL.nombre, categoriaF.puntuacion)
            
    for origenF in form.puntuacionOrigenLicor_set.all():
        puntuacion=puntuacion+getPuntuacionAtributo(origenF.origen,licor.origen, origenF.puntuacion)
        
    for marcaF in form.puntuacionMarcaLicor_set.all():
        puntuacion=puntuacion+getPuntuacionAtributo(marcaF.marca,licor.titulo, marcaF.puntuacion)
        
    return {licor.i:puntuacion}
    