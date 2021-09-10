"""Contratos urls."""

# Django
from django.urls import path
from contratos import views


urlpatterns = [
    path(
        route='plantilla/list/',
        view=views.PlantillaListView.as_view(),
        name="list-plantilla"
    ),
    path(
        route='plantilla/create/',
        view=views.create_plantilla,
        name="create-plantilla"
    ),
    path(
        route='<int:plantilla_id>/plantilla/update/',
        view=views.update_plantilla,
        name="update-plantilla"
    ),
    path(
        route='<int:object_id>/plantilla/delete/',
        view=views.delete_plantilla,
        name="delete-plantilla"
    ),
    path(
        route='list/',
        view=views.ContratoListView.as_view(),
        name="list"
    ),
    path(
        route='<int:pk>/detail/',
        view=views.ContratoDetailView.as_view(),
        name="detail"
    ),
    
]
