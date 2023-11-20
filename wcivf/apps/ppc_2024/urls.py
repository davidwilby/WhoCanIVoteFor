from django.urls import path

from .views import PCC2024DetailView, PCC2024HomeView

urlpatterns = [
    path(
        "",
        PCC2024HomeView.as_view(),
        name="home",
    ),
    path(
        "details/",
        PCC2024DetailView.as_view(),
        name="details",
    ),
]
