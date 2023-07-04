from django.urls import path
from . import views

urlpatterns = [
    path("sectors", views.sectors_list, name="sectors"),
    path("words", views.words_list, name="words"),
    path("game", views.game, name="game"),
    path("", views.index, name="index")
]
