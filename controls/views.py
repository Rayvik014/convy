from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sector, Word

class SectorListView(ListView):
    model = Sector
    queryset = Sector.objects.all()

class WordListView(ListView):
    model = Word
    queryset = Word.objects.all()

class SectorDetailView(DetailView):
    model = Sector

class WordDetailView(DetailView):
    model = Word