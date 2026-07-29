from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    # Visit CRUD
    path('', views.visit_list, name='list'),
    path('create/', views.visit_create, name='create'),
    path('<int:pk>/', views.visit_detail, name='detail'),
    path('<int:pk>/edit/', views.visit_update, name='update'),
    path('<int:pk>/delete/', views.visit_delete, name='delete'),

    # Medical records
    path('<int:pk>/exam-notes/', views.add_exam_notes, name='add_exam_notes'),
    path('<int:pk>/manipulation/', views.add_manipulation, name='add_manipulation'),
    path('<int:pk>/vaccination/', views.add_vaccination, name='add_vaccination'),
    path('<int:pk>/prescription/', views.add_prescription, name='add_prescription'),
    path('<int:pk>/lab-result/', views.add_lab_result, name='add_lab_result'),
    path('<int:pk>/attachment/', views.add_attachment, name='add_attachment'),
    path('<int:pk>/deworming/', views.add_deworming, name='add_deworming'),

    # History views
    path('patient/<int:patient_pk>/prescriptions/', views.prescription_history, name='prescription_history'),
    path('patient/<int:patient_pk>/vaccinations/', views.vaccination_history, name='vaccination_history'),
    path('patient/<int:patient_pk>/dewormings/', views.deworming_history, name='deworming_history'),

    # Autocomplete endpoints
    path('manipulation-autocomplete/', views.manipulation_autocomplete, name='manipulation_autocomplete'),
]
