from whoosh import index
import os
from whooshLicor.schemas import crear_esquema
import django
from django.core.paginator import Paginator
django.setup()
from licor.models import Licor

def indexar():
    if not os.path.exists("licoresIndex"):
        os.mkdir("licoresIndex")
    
    index.create_in("licoresIndex", crear_esquema())
    

    ix = index.open_dir("licoresIndex")
    writer = ix.writer()
    
    licores = Licor.objects.all().order_by('id')
    
    
    paginator = Paginator(licores, 20)
    
    licores = paginator.page(1)
    while licores.has_next():
        for licor in licores:
            i = licor.id
            t = licor.titulo.strip()
            d = licor.descripcion
            p = licor.precio
            o = licor.origen
            grad = licor.graduacion
            es = licor.enStock
            url = licor.urlProducto
            cat = array_toString(list(licor.categoria_set.all()))
            print(cat)
            writer.add_document(id= i, categoria = cat,titulo = t,descripcion = d,precio = p, 
                                origen = o,graduacion = grad, enStock= es,urlProducto=url)
       
        licores = paginator.page(licores.next_page_number())
    writer.commit()

def array_toString(array):
    result = ""
    for a in array:
        result= result + str(a.nombre) + " "
    return result
indexar()
    