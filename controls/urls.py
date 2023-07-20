from django.urls import path
from . import views

urlpatterns = [
    path("game/", views.game, name="game"),
    path("", views.index, name="index"),
    path("game/PlusOneWord", views.button_plus_one, name="PlusOneWord"),
    path("game/PlusTenWords", views.button_plus_ten, name="PlusTenWords"),
    path("game/answer", views.answer, name="answer"),
    path("login/", views.my_login, name="login"),
    path("logout/", views.my_logout, name="logout"),
    path("registration/", views.registration, name="registration")

]
