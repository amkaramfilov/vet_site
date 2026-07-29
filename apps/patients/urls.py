from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='list'),
    path('create/', views.patient_create, name='create'),
    path('search/', views.patient_search, name='search'),
    path('species-autocomplete/', views.species_autocomplete, name='species_autocomplete'),
    path('breed-autocomplete/', views.breed_autocomplete, name='breed_autocomplete'),
    path('<int:pk>/', views.patient_detail, name='detail'),
    path('<int:pk>/edit/', views.patient_update, name='update'),
    path('<int:pk>/delete/', views.patient_delete, name='delete'),
    path('<int:pk>/weight/add/', views.add_weight, name='add_weight'),
    path('<int:pk>/weight/history/', views.weight_history, name='weight_history'),
]
