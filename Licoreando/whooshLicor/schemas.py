'''
Created on 20 ene. 2019

@author: viento
'''
from whoosh import fields


def crear_esquema():
    licorSchema = fields.Schema(
        id = fields.NUMERIC(stored=True),
    titulo = fields.TEXT(stored = True,sortable = True,field_boost=1.5),
    descripcion = fields.TEXT,
    categoria = fields.TEXT(sortable = True),
    precio = fields.NUMERIC(sortable= True),
    origen = fields.TEXT(sortable= True),
    graduacion = fields.NUMERIC(sortable = True),
    enStock = fields.BOOLEAN(stored = True),
    urlProducto = fields.TEXT(field_boost=0.5),)
    
    return licorSchema