from bs4 import BeautifulSoup
import urllib.request

import re

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r


def numero_paginas(url='https://marianomadrueno.es/tienda/'):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find('ul',class_='page-numbers').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_licores():
    nPaginas=numero_paginas()
    licores_marianomadrueno=[]
    for i in range(1,3):
        
        soup=BeautifulSoup(abrir_url( 'https://marianomadrueno.es/tienda/page/'+str(i) ),'html.parser')
        
        for licor in soup.find_all("a",class_="woocommerce-LoopProduct-link woocommerce-loop-product__link"):
            
            licorUrl=licor['href']
            
            licorSoup=BeautifulSoup(abrir_url(licorUrl),'lxml')
            
            
            titulo = licorSoup.find_all('h1',class_='product_title entry-title')[0].text
            print(titulo)
            precio = float(licorSoup.find_all('p',class_='price')[0].span.text.split('€')[0].replace(',','.'))
            print(precio)
            referencia = None
            origen= "Desconocido"
            meta=licorSoup.find_all('div',class_='product_meta')[0].text.split(':')
            palabraAnterior=""
            categoria=[]
            
            for palabra in meta:
                if("Referencia" in palabraAnterior):
                    referencia = palabra.strip()
                if("Procedencia" in palabraAnterior):
                    origen = palabra.strip().replace('Referencia','')
                if("Categoría" in palabraAnterior):
                    categoria=palabra.upper().split('\n')[0].split(',')
                    for index in range(0,len(categoria)):
                        categoria[index] = categoria[index].strip()
                palabraAnterior = palabra
                
            print(referencia)
            print(origen)
            print(categoria)
            
            urlImagen = licorSoup.find_all('img',class_='wp-post-image')[0]['src']
            print(urlImagen)
            
            descripcionArray = licorSoup.find_all('div',class_='woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab')
            if(len(descripcionArray)>0):
                descripcionArray = descripcionArray[0].find_all('p')#,{'style': re.compile(r'text-align*')})
            descripcion=""
            for p in descripcionArray:
                descripcion=descripcion+'\n'+p.text.strip()
            print(descripcion)
            
            
            graduacion=None
            
            if("%" in descripcion and "GRAD" in descripcion.upper()):
                graduacion=descripcion.split("%")[-2].split(" ")[-1]
                
                if ( not graduacion.strip().isdigit() ):
                    graduacion=None
                else:
                    graduacion=float(graduacion)
                    
            print(graduacion)
            enStock = True
            stock=licorSoup.find_all('p',class_='stock in-stock')
                       
            if (len(stock)!=0):
                stock=int(stock[0].text.strip().split(' ')[0])
            else:
                stock=0
                
            if (stock<=0):
                enStock=False
          
            print(enStock)
            
            peso = licorSoup.find_all('td',class_='product_weight')[0].text.strip()
            
            print(peso)
            diccionarioLicor = {"codigoReferencia":referencia,"titulo":titulo,"descripcion":descripcion,"precio":precio,"origen":origen,"categoria":categoria,"cantidad":peso,"graduacion":graduacion,"urlProducto":licorUrl,"enStock":enStock,"urlImagen":urlImagen}
            licores_marianomadrueno.append(diccionarioLicor)
    return licores_marianomadrueno
extraer_licores()        
        
        
        
