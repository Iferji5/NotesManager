from django.urls import path
from . import views


urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Notes CRUD
    path('', views.notes_list, name='notes_list'),
    path('note/create/', views.note_create, name='note_create'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),

 # Ruta para actualizar la posición
    path('update-position/', views.update_note_position, name='update_note_position'),
]

