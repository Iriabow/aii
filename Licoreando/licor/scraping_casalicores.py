import os

import urllib.request

from bs4 import BeautifulSoup

dirdocs="licores"
dirindex="Index"

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def numero_paginas(url):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find(class_='page-numbers').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_texto_casalicores():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    
    paginas = numero_paginas('http://lacasadeloslicores.es/tienda/')
    licores_casalicores=[]
    for i in range(1,2):#paginas+1):
        soup=BeautifulSoup(abrir_url('http://lacasadeloslicores.es/tienda/page/'+str(i)+"/"),'html.parser')
        
        for enlace in soup.find_all('div',class_='archive-products'):
            
            tupla = []
            urlImagen = enlace.find(class_= "inner").img['src']
            url = enlace.find(class_="product-image").a['href']
            
            soup2 = BeautifulSoup(abrir_url(url),'html.parser')
            
            producto = soup2.find(itemtype = 'http://schema.org/Product')
            
            titulo = producto.find(itemprop='name').text

            descripcionEntera = producto.find(class_="resp-tabs-container")
            
            descripcion = descripcionEntera.text.split("Reseñas")[0].strip()
            
            descripcion = descripcion.split('CATA')[0].strip()
            descripcion = descripcion.split('Tipo')[0].strip()

            
            
            producto2 = soup2.find(class_="product-summary-wrap")
            referencia = producto2.find(class_="sku").text
            
            precio = producto2.find(class_="price").text
          
            urlStock = producto.find(itemprop="availability")
             
            if urlStock != None:
                urlStock = urlStock['href']
                
            enStock = True
            
            if(urlStock != 'http://schema.org/InStock'):
                enStock= False
            
            try:
                categoria = producto2.find(class_="posted_in").text.split('Categoría:')[1].strip()
            except:
                categoria = "OTROS LICORES"
            
            try:
                volumen = producto.find(class_="goog-text-highlight")[0].text
                
            except:
                volumen = "Sin determinar"
            
            try:
                graduacion = producto.find(class_="goog-text-highlight")[1].text
                
            except:
                graduacion = "Sin determinar"
                
         
            #tupla = (referencia,titulo,descripcion,precio,categoria,volumen,graduacion,url,enStock,urlImagen)
            categoria=[categoria]
            diccionarioLicor = {"codigoReferencia":referencia,"titulo":titulo,"descripcion":descripcion,"precio":precio,"origen":"Desconocido","categoria":categoria,"cantidad":volumen,"graduacion":graduacion,"urlProducto":url,"enStock":enStock,"urlImagen":urlImagen}
            print(diccionarioLicor)
            licores_casalicores.append(diccionarioLicor)
    return licores_casalicores
if __name__ == '__main__':
    
    extraer_texto_casalicores()
    
    