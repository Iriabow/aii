#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    
    for i in range(1,paginas):
        soup=BeautifulSoup(abrir_url('https://www.disevil.com/tienda/es/80-licores-y-destilados/?p='+str(i)+"/"),'html.parser')
        for story in soup.find_all('div',class_='story'):
            
            antetitulo = story.find(class_='ant').string
        
            '''
            titulo= story.find(class_='scnt').a.text
            '''
           
            enlaceImagen=story.a.img['src']
            descripcion=story.find(class_='desc').text
            fechaPublicacion=story.find(class_='fec').text
            fecha = fechaPublicacion.split("(")
            fechaPublicacion = fecha[0].strip()
            dia=int(fechaPublicacion.split(" ")[0])
            mes=fechaPublicacion.split(" ")[2]
            a�o=int(fechaPublicacion.split(" ")[3])
            diccionarioMes={"Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6,"Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"noviembre":11,"Diciembre":12}
            mes= int(diccionarioMes[mes])
            fechaDateTime = datetime.datetime(a�o,mes,dia)
            tupla = (antetitulo,titulo,enlaceImagen,descripcion,str(fechaDateTime))
            file = open("noticias/ecartelera" + str(numeracion)+".txt", "w",encoding="utf-8")
            numeracion=numeracion+1   
            for i in tupla:    
                file.write(i+"\n")
            file.close()

def cargar():
    if not os.path.exists(dirdocs):
        os.mkdir(dirdocs)
    extraer_texto()
    ix = create_in(dirindex, schema=get_schema())
    writer = ix.writer()
    i=0
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs+docname):
            add_doc(writer, dirdocs, docname)
            i+=1
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " noticias")
    writer.commit()

def buscar_titulo_descripcion():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query =MultifieldParser(["titulo", "descripcion"], ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                print(r)
                lb.insert(END,"Antet�tulo: "+r['anteTitulo'][1:])
                lb.insert(END,"T�tulo: "+r['titulo'][1:])
                lb.insert(END,"Enlace a la imagen: "+r['link'][1:])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por t�tulo y/o descripci�n")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el t�tulo y/o descripci�n de la noticia:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT) 
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview) 
    
def buscar_fecha():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        print(en)
        with ix.searcher() as searcher:
            query = QueryParser('fecha', ix.schema).parse("fecha:[]")
            results = searcher.search(query)
            for r in results:
                print(r)
                lb.insert(END,"T�tulo: "+r['titulo'][1:].encode('latin1').decode('utf8'))
                lb.insert(END,"Fecha: "+r['fecha'][1:])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por rango de fechas")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el rango de fechas separados por un espacio y el formato YYYYMMDD:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)   
    
def buscar_descripcion():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser('descripcion', ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                print(r)
                lb.insert(END,"Antetitulo: "+r['anteTitulo'][1:])
                lb.insert(END,"T�tulo: "+r['titulo'][1:])
                lb.insert(END,"Enlace a la imagen: "+r['link'][1:])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por descripci�n")
    f =Frame(v);
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el texto de la descripci�n:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)   

def get_schema():
    return Schema(anteTitulo=TEXT(stored=True), titulo=TEXT(stored=True), link=TEXT(stored=True),
                   descripcion=TEXT(stored=True), fecha=whoosh.fields.NUMERIC(stored=True))
#TEner en cuenta el KEYWORD y el DATETIME

def add_doc(writer, path, docname):
    fileobj=open(path+'/'+docname, "rb")
    # IMPORTANTE: Convertir el contenido del fichero a Unicode
    at=str(fileobj.readline().strip())
    t=str(fileobj.readline().strip())
    l=str(fileobj.readline().strip())
    d=str(fileobj.readline())
    f=str(fileobj.readline().strip())[2:]
    fecha=f.split(" ")[0]
    fechaS=fecha.split("-")
    fechaP=str(fechaS[0])+str(fechaS[1])+str(fechaS[2])
    fechaP=int(fechaP)
    fileobj.close()           
    writer.add_document(anteTitulo=at, titulo=t, link=l,
                   descripcion=d, fecha=fechaP)  

if __name__ == '__main__':
    top = Tk()
    menu = Menu(top)
    
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar", command=cargar)
    menudatos.add_command(label="Salir", command=top.quit)
    menu.add_cascade(label="Datos",menu = menudatos)
    
    menuBuscar = Menu(menu, tearoff=0)
    menuBuscar.add_command(label="T�tulo y Descripci�n", command=buscar_titulo_descripcion)
    menuBuscar.add_command(label="Fecha", command=buscar_fecha)
    menuBuscar.add_command(label="Descripci�n", command=buscar_descripcion)
    menu.add_cascade(label="Buscar",menu = menuBuscar)
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


dirdocs="noticias"
dirindex="Index"

def abrir_url(url):
    r = urllib.request.urlopen(url)
    return r

def extraer_texto():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    numeracion =1
    for i in range(1,4):
        soup=BeautifulSoup(abrir_url('https://www.ecartelera.com/noticias/lista/'+str(i)+"/"),'html.parser')
        for story in soup.find_all('div',class_='story'):
            
            antetitulo = story.find(class_='ant').string
            '''
            antetitulo=antetitulo.replace("�","u")
            antetitulo=antetitulo.replace("�","u")
            antetitulo=antetitulo.replace("�","i")
            antetitulo=antetitulo.replace("�","e")
            antetitulo=antetitulo.replace("�","a")
            antetitulo=antetitulo.replace("�","o")
            antetitulo=antetitulo.replace("�","n")
            antetitulo=antetitulo.replace("�","N")
            antetitulo=antetitulo.replace("�","")
            antetitulo=antetitulo.replace("�","")
            '''
            titulo= story.find(class_='scnt').a.text
            '''
            titulo=titulo.replace("�","u")
            titulo=titulo.replace("�","u")
            titulo=titulo.replace("�","i")
            titulo=titulo.replace("�","e")
            titulo=titulo.replace("�","a")
            titulo=titulo.replace("�","o")
            titulo=titulo.replace("�","n")
            titulo=titulo.replace("�","")
            titulo=titulo.replace("�","")
            '''
            enlaceImagen=story.a.img['src']
            descripcion=story.find(class_='desc').text
            fechaPublicacion=story.find(class_='fec').text
            fecha = fechaPublicacion.split("(")
            fechaPublicacion = fecha[0].strip()
            dia=int(fechaPublicacion.split(" ")[0])
            mes=fechaPublicacion.split(" ")[2]
            a�o=int(fechaPublicacion.split(" ")[3])
            diccionarioMes={"Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6,"Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"noviembre":11,"Diciembre":12}
            mes= int(diccionarioMes[mes])
            fechaDateTime = datetime.datetime(a�o,mes,dia)
            tupla = (antetitulo,titulo,enlaceImagen,descripcion,str(fechaDateTime))
            file = open("noticias/ecartelera" + str(numeracion)+".txt", "w",encoding="utf-8")
            numeracion=numeracion+1   
            for i in tupla:    
                file.write(i+"\n")
            file.close()

def cargar():
    if not os.path.exists(dirdocs):
        os.mkdir(dirdocs)
    extraer_texto()
    ix = create_in(dirindex, schema=get_schema())
    writer = ix.writer()
    i=0
    for docname in os.listdir(dirdocs):
        if not os.path.isdir(dirdocs+docname):
            add_doc(writer, dirdocs, docname)
            i+=1
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " noticias")
    writer.commit()

def buscar_titulo_descripcion():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query =MultifieldParser(["titulo", "descripcion"], ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                print(r)
                lb.insert(END,"Antet�tulo: "+r['anteTitulo'][1:])
                lb.insert(END,"T�tulo: "+r['titulo'][1:])
                lb.insert(END,"Enlace a la imagen: "+r['link'][1:])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por t�tulo y/o descripci�n")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el t�tulo y/o descripci�n de la noticia:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT) 
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview) 
    
def buscar_fecha():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        print(en)
        with ix.searcher() as searcher:
            query = QueryParser('fecha', ix.schema).parse("fecha:[]")
            results = searcher.search(query)
            for r in results:
                print(r)
                lb.insert(END,"T�tulo: "+r['titulo'][1:].encode('latin1').decode('utf8'))
                lb.insert(END,"Fecha: "+r['fecha'][1:])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por rango de fechas")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el rango de fechas separados por un espacio y el formato YYYYMMDD:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)   
    
def buscar_descripcion():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser('descripcion', ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                print(r)
                lb.insert(END,"Antetitulo: "+r['anteTitulo'][1:])
                lb.insert(END,"T�tulo: "+r['titulo'][1:])
                lb.insert(END,"Enlace a la imagen: "+r['link'][1:])
                lb.insert(END,'')
    v = Toplevel()
    v.title("Busqueda por descripci�n")
    f =Frame(v);
    f.pack(side=TOP)
    l = Label(f, text="Introduzca el texto de la descripci�n:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)   

def get_schema():
    return Schema(anteTitulo=TEXT(stored=True), titulo=TEXT(stored=True), link=TEXT(stored=True),
                   descripcion=TEXT(stored=True), fecha=whoosh.fields.NUMERIC(stored=True))
#TEner en cuenta el KEYWORD y el DATETIME

def add_doc(writer, path, docname):
    fileobj=open(path+'/'+docname, "rb")
    # IMPORTANTE: Convertir el contenido del fichero a Unicode
    at=str(fileobj.readline().strip())
    t=str(fileobj.readline().strip())
    l=str(fileobj.readline().strip())
    d=str(fileobj.readline())
    f=str(fileobj.readline().strip())[2:]
    fecha=f.split(" ")[0]
    fechaS=fecha.split("-")
    fechaP=str(fechaS[0])+str(fechaS[1])+str(fechaS[2])
    fechaP=int(fechaP)
    fileobj.close()           
    writer.add_document(anteTitulo=at, titulo=t, link=l,
                   descripcion=d, fecha=fechaP)  

if __name__ == '__main__':
   print(numero_paginas('https://www.disevil.com/tienda/es/80-licores-y-destilados/'))
