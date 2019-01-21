'''
~
'''
from whoosh import sorting, qparser
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.query import Regex,And,Or,Not,FuzzyTerm,Term
#Range facets
#facet= getPrecioFacet()
#results = searcher.search(myquery, groupedby=facet)
#results.groups(), devuelve un diccionario con los grupos.
def getPrecioFacet():
    return sorting.RangeFacet("precio", 0, 10000, [10, 40, 50, 100]) # 0-10€, 10-50€, 50-100€ y ya de 100 en 100.

def getGraduaciónFacet():
    return sorting.RangeFacet("graduación", 0, 100, [5, 10],hardend=True)


def faceta_enStock():
    faceta_enStock = sorting.FieldFacet('enStock', reverse = True)
    return faceta_enStock

def faceta_categoria():
    faceta_categoria = sorting.FieldFacet('categoria')
    return faceta_categoria

def ordenarLista(orderDic):
    
    
def listarPorAtributo(busqueda="",categoria=None, orderDic):
    
    ix=index.open_dir("licoresIndex")
    busqueda = busqueda.strip()
    with ix.searcher() as searcher:
    
        if(not(busqueda) and not(categoria)):
            query = QueryParser("titulo",ix.schema).parse("*")
        elif(not(busqueda) and categoria):
            query = QueryParser("titulo",ix.schema).parse("*") & queryCategoryGenerator(categoria)
        elif(busqueda and not(categoria)):
            query = querySearchGenerator(busqueda)
        elif(busqueda and categoria):
            query = querySearchGenerator(busqueda) & queryCategoryGenerator(categoria)
        
        query.normalize()
        scores = sorting.ScoreFacet()
        results = searcher.search(query,sortedby=[faceta_enStock(), scores],limit = 3000)
        print(results)
        for r in results:
            print(r)
        
def querySearchGenerator(busqueda):
    trozos = busqueda.split(" ")
    query = None
    for p in trozos:
        if(query is None):
            query = FuzzyTerm("titulo",p,maxdist=int(p/4)) | FuzzyTerm("descripcion",p,maxdist=int(p/4))
        else:
            query = query | FuzzyTerm("titulo",p,maxdist=int(p/4)) | FuzzyTerm("descripcion",p,maxdist=int(p/4))
    print(query)
    return query

def queryCategoryGenerator(busqueda):
    trozos = busqueda
    query = None
    for p in trozos:
        if(query is None):
            query = FuzzyTerm("categoria",p,maxdist=int(p/4))
        else:
            query = query | FuzzyTerm("categoria",p,maxdist=int(p/4))
    
    return query
listarPorAtributo()
                
#Ordenar/agrupar con varias "facetas", las facetas se usan para ordenar y agrupar.
"""

MultiFacet

This facet type returns a composite of the keys returned by two or more sub-facets, allowing you to sort/group by the intersected values of multiple facets.

MultiFacet has methods for adding facets:

myfacet = sorting.RangeFacet(0, 1000, 10)

mf = sorting.MultiFacet()
mf.add_field("category")
mf.add_field("price", reverse=True)
mf.add_facet(myfacet)
mf.add_score()

You can also pass a list of field names and/or FacetType objects to the initializer:

prices = sorting.FieldFacet("price", reverse=True)
scores = sorting.ScoreFacet()
mf = sorting.MultiFacet(["category", prices, myfacet, scores])
"""
#Comparando dos formas de hacer las cosas:
"""

mf = sorting.MultiFacet()
mf.add_field("size")
mf.add_field("price", reverse=True)
results = searcher.search(myquery, sortedby=mf)

# or...
sizes = sorting.FieldFacet("size")
prices = sorting.FieldFacet("price", reverse=True)
results = searcher.search(myquery, sortedby=[sizes, prices])

"""