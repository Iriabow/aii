from django.shortcuts import render, get_object_or_404

from licor.forms import SearchForm
from licor.models import Licor

def index(request): 
    return render(request,'index.html')

def buscarLicor(request):
    if request.method=='POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['Título']
            precio = form.cleaned_data['Precio']
            graduacion = form.cleaned_data['Graduación']
            procedencia = form.cleaned_data['Procedencia']
            categoria = form.cleaned_data['Categoría']
            licores = Licor.objects.all()
            form=SearchForm()
            return render(request,'search_licor.html', {'licores':licores,'form':form })
    form=SearchForm()
    licores = Licor.objects.all()
    return render(request,'search_licor.html', {'form':form,'licores':licores})

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