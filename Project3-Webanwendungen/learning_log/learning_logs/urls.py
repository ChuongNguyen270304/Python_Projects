"""Define URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Start-seite
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Seite zum Hinzufügen neuer Fachgebiete
    path('new_topic/', views.new_topic, name='new_topic'),
    # Seite zum Hinzufügen neuer Einträge für ein bestimmtes Fachgebiet
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Seite zum Bearbeiten eines Eintrags
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
