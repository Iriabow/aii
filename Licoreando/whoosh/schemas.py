'''
Created on 20 ene. 2019

@author: viento
'''
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC, BOOLEAN

class LicorSchema(SchemaClass):
    id = NUMERIC(Store=True)
    titulo = TEXT(sortable=True,field_boost=1.5)
    descripcion = TEXT
    precio = NUMERIC(sortable=True)
    origen = TEXT(sortable=True)
    graduacion = NUMERIC(sortable=True)
    enStock = BOOLEAN(sortable=True)
    urlProducto = TEXT(field_boost=0.5)