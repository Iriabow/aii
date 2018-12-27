from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import re

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def abrir_url_procesado(url):
    driver = webdriver.Firefox(executable_path=r'../lib/geckodriver')
    driver.get(url)
    html = driver.page_source
    return html
def numero_paginas(url='https://marianomadrueno.es/tienda/'):
    soupAux = BeautifulSoup(abrir_url(url),'html.parser')
    numeroPaginas = soupAux.find('ul',class_='page-numbers').find_all('li')[-2].text
    return int(numeroPaginas)

def extraer_licores():
    nPaginas=numero_paginas()

    for i in range(1,nPaginas+1):
        
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
            
            descripcionArray = licorSoup.find_all('div',class_='woocommerce-tabs wc-tabs-wrapper')[0]
        
            descripcionArray = descripcionArray.find_all('p',{'style': re.compile(r'text-align*')})
            descripcion=""
            for p in descripcionArray:
                descripcion=descripcion+p.text
            print(descripcion)
            
            enStock = True
            stock=licorSoup.find_all('p',class_='stock in-stock')
                       
            if (len(stock)!=0):
                stock=int(stock[0].text.strip().split(' ')[0])
            else:
                stock=0
                
            if (stock<=0):
                enStock=False
          
            print(enStock)
          

            
extraer_licores()        
        
        
        
