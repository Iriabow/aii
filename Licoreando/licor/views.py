from django.shortcuts import render, get_object_or_404

from licor.forms import SearchForm
from licor.models import Licor, Categoria
from whooshLicor.utils import listarPorAtributo


def index(request): 
    return render(request,'index.html')

def buscarLicor(request):
    form=SearchForm()
    categorias = Categoria.objects.all()
    if request.method=='POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            busqueda = form.cleaned_data["busqueda"]
            graduacionMinima = form.cleaned_data["graduacionMinima"]
            graduacionMaxima = form.cleaned_data["graduacionMaxima"]
            precioMinimo = form.cleaned_data["precioMinimo"]
            precioMaximo = form.cleaned_data["precioMaximo"]
            print(busqueda,"+",graduacionMinima,"+",graduacionMaxima,"+",precioMinimo,"+",precioMaximo)
#             ordenarSimilitud = form.cleaned_data["ordenarSimilitud"]
#             ordenarPrecio = form.cleaned_data["ordenarPrecio"]
#             ordenarTitulo = form.cleaned_data["ordenarTitulo"]
#             ordenarGraduacion = form.cleaned_data["ordenarGraduacion"]
#             ordenarProcedencia = form.cleaned_data["ordenarProcedencia"]
#            categoria = form.cleaned_data["Categoría"]           
#            licoresId = listarPorAtributo(busqueda=busqueda,categoria=[], order ="",groupDic={}, nElementosPagina=20, pagina=1)
#            licores = getLicores(licoresId)
            licores = []
            return render(request,'search_licor.html', {'licores':licores,'form':form ,'categorias': categorias})
    licoresId = listarPorAtributo()
    licores = getLicores(licoresId)
    return render(request,'search_licor.html', {'form':form,'licores':licores, 'categorias': categorias})

def recomendacion(request):
    return render(request,'index.html')

'''
def listarLicor(request):
    licores = []
    if request.method=='GET':
        licores = Licor.objects.all().order_by('titulo')
    return render(request,'list.html', {'licores': licores})
    
def parecidoLicor(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
            items=[]
            for re in recommended:
                item = Film.objects.get(pk=int(re[1]))
                items.append(item)
            return render(request,'similarFilms.html', {'film': film,'films': items})
    form = FilmForm()
    return render(request,'search_film.html', {'form': form})

def recomendarLicor(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
            items=[]
            for re in recommended:
                item = Film.objects.get(pk=int(re[1]))
                items.append(item)
            return render(request,'similarFilms.html', {'film': film,'films': items})
    form = FilmForm()
    return render(request,'search_film.html', {'form': form})
'''
def getLicores(licoresId):
    licores = []
    for licor in licoresId[0]:
        licores.append(Licor.objects.get(id=licor['id'])) 
    return licores