from django.shortcuts import render
from .models import Sector, Word

def sectors_list(request):
    sectors = Sector.objects.all()
    return render(request, 'controls/Sectors_List.html', {'sectors': sectors})

def words_list(request):
    words = Word.objects.all()
    return render(request, 'controls/Words_List.html', {'words': words})

def game(request):
    return render(request, 'controls/Game.html')

def index(request):
    return render(request, 'controls/Index.html')