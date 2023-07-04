from django.shortcuts import render
from .models import Sector, Word, Progress

def sectors_list(request):
    sectors = Sector.objects.all()
    return render(request, 'controls/Sectors_List.html', {'sectors': sectors})

def words_list(request):
    words = Word.objects.all()
    return render(request, 'controls/Words_List.html', {'words': words})

def progress(request):
    progress = Progress.objects.all()
    return render(request, 'controls/Progress.html', {'progress': progress})

def game(request):
    return render(request, 'controls/Game.html')

def index(request):
    return render(request, 'controls/Index.html')