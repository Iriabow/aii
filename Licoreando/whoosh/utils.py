'''
Created on 20 ene. 2019

@author: viento
'''
from whoosh import sorting

#Range facets
#facet= getPrecioFacet()
#results = searcher.search(myquery, groupedby=facet)
#results.groups(), devuelve un diccionario con los grupos.
def getPrecioFacet():
    return sorting.RangeFacet("precio", 0, 10000, [10, 40, 50, 100], allow_overlap=True) # 0-10€, 10-50€, 50-100€ y ya de 100 en 100.

def getGraduaciónFacet():
    return sorting.RangeFacet("gradución", 0, 100, [5, 10],hardend=True, allow_overlap=True)


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