from licor.models import Licor
from licor.scraping_casalicores import extraer_texto_casalicores
from licor.scraping_disevil import extraer_texto_disevil
from licor.scraping_marianomadrueno import extraer_licores

def save_all_licores():
    for licDicc in (extraer_texto_casalicores()):
        save_licor(licDicc)
        
    for licDicc in (extraer_texto_disevil()):
        save_licor(licDicc)
        
    for licDicc in (extraer_licores()):
        save_licor(licDicc)


def save_licor(licDicc):
    
    licor = Licor(codigoReferencia=licDicc["codigoReferencia"],
                  titulo=licDicc["titulo"],
                  descripcion=licDicc["descripcion"],
                  precio=licDicc["precio"],
                  origen=licDicc["origen"],
                  cantidad=licDicc["cantidad"],
                  graduacion=licDicc["graduacion"],
                  urlProducto=licDicc["urlProducto"],
                  urlImagen=licDicc["urlImagen"],
                  enStock=licDicc["enStock"],
                  )
    
save_all_licores()