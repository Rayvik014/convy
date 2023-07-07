from django.urls import path
from . import views

urlpatterns = [
    path("game", views.game, name="game"),
    path("", views.index, name="index"),
    path("PlusOneWord", views.button_plus_one),
    path("answer", views.answer)
]
