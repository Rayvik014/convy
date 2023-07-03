from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.SectorListView.as_view(),
        name="sectors-list"
    ),
    path(
        "controls/<int:pk>",
        views.SectorDetailView.as_view(),
        name="sectors-detail"
    )
]
