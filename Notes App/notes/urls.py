from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('add/', views.add_note, name='add_note'),
    path('delete/<int:pk>/', views.delete_note, name='delete_note'),
]
