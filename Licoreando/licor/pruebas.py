import datetime
import os
from time import strptime, strftime
from tkinter import *
from tkinter import messagebox
import urllib.request

from bs4 import BeautifulSoup
import whoosh
from whoosh.fields import TEXT, Schema, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.qparser.default import MultifieldParser, QueryParser


dirdocs="licores"
dirindex="Index"

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def numero_paginas(url):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find('ul',class_='pagination').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_texto():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    numeracion = 1
    paginas = numero_paginas('https://www.disevil.com/tienda/es/80-licores-y-destilados/')
    
    for i in range(1,paginas+1):
        soup=BeautifulSoup(abrir_url('https://www.disevil.com/tienda/es/80-licores-y-destilados/?p='+str(i)+"/"),'html.parser')
        
        for enlace in soup.find_all(class_='quick-view'):
            
            url = enlace['href']
            print(url)
            soup2 = BeautifulSoup(abrir_url(url),'html.parser')
            
            producto = soup2.find(itemtype="http://schema.org/Product")
            
            titulo = producto.find(itemprop="name").text
            print(titulo)
            
            descripcion = producto.find(itemprop="description")
            if(descripcion !=None):
                descripcion = descripcion.text
            else:
                descripcion=""
            precio= producto.find(itemprop="price").text
            
            print(precio)
            referencia= producto.find(itemprop="sku").text
            print(referencia)
            enlace=url
            
            urlImagen=producto.find(itemprop="image")['src']
            
            urlStock = producto.find(itemprop="availability")
            if urlStock != None:
                urlStock = urlStock['href']
                
            enStock = True
            
            if(urlStock != 'http://schema.org/InStock'):
                enStock= False
                
            print(enStock)
                
            #for description in producto.find_all(class_='rte'):
                
             #   categoria=
              #  volumen=
               # origen= 
               # graduacion=
                
               # enStock=
            
            
            
            
            
           
           
            
            
            
    print(numeracion)
if __name__ == '__main__':
    
    
    print(numero_paginas('https://www.disevil.com/tienda/es/80-licores-y-destilados/'))
    extraer_texto()
    