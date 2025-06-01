# notes_app/views.py

import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Note
from .forms import SignUpForm, NoteForm


# =====================================================
#        VISTAS PARA AUTENTICACIÓN DE USUARIO
# =====================================================

def signup_view(request):
    """
    Vista para registrar nuevos usuarios.
    - Si el método es POST, procesa el formulario SignUpForm.
    - Si el formulario es válido, crea el usuario, lo autentica y redirige a notes_list.
    - Si es GET, muestra el formulario vacío.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()           # Crea el usuario (hashea la contraseña)
            login(request, user)         # Inicia sesión automáticamente
            return redirect('notes_list')
    else:
        form = SignUpForm()

    return render(request, 'notes_app/signup.html', {'form': form})


def login_view(request):
    """
    Vista para iniciar sesión.
    - Si el método es POST, procesa AuthenticationForm con los datos recibidos.
    - Si las credenciales son correctas, autentica al usuario y redirige a notes_list.
    - Si es GET, muestra el formulario de login vacío.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()      # Obtiene el usuario autenticado
            login(request, user)        # Crea la sesión del usuario
            return redirect('notes_list')
    else:
        form = AuthenticationForm()

    return render(request, 'notes_app/login.html', {'form': form})


def logout_view(request):
    """
    Vista para cerrar sesión.
    - Si el método es POST, destruye la sesión y redirige a login.
    - Si es GET, muestra una página de confirmación de logout.
    """
    if request.method == 'POST':
        logout(request)                 # Destruye la sesión actual
        return redirect('login')

    return render(request, 'notes_app/logout.html')


# =====================================================
#     VISTAS PARA CRUD DE NOTAS (require login)
# =====================================================

@login_required(login_url='login')
def notes_list(request):
    """
    Muestra la lista de notas pertenecientes al usuario autenticado.
    - Filtra las notas por request.user y ordena por fecha de actualización descendente.
    """
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'notes_app/notes_list.html', {'notes': notes})


@login_required(login_url='login')
def note_detail(request, pk):
    """
    Muestra el detalle de una nota específica.
    - get_object_or_404 asegura que solo el dueño de la nota pueda verla.
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes_app/note_detail.html', {'note': note})


@login_required(login_url='login')
def note_create(request):
    """
    Permite crear una nueva nota.
    - Si el método es POST, procesa NoteForm con los datos recibidos.
    - Si el formulario es válido, asigna request.user como dueño y guarda la nota.
    - Si es GET, muestra el formulario vacío para crear una nota.
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            return redirect('notes_list')
    else:
        form = NoteForm()

    return render(request, 'notes_app/note_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required(login_url='login')
def note_edit(request, pk):
    """
    Permite editar una nota existente.
    - Recupera la nota con get_object_or_404 asegurando request.user.
    - Si es POST, actualiza los campos de la nota. Si es GET, precarga el formulario.
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes_app/note_form.html', {
        'form': form,
        'action': 'Edit'
    })


@login_required(login_url='login')
def note_delete(request, pk):
    """
    Permite eliminar una nota existente.
    - Recupera la nota asegurando que pertenezca a request.user.
    - Si es POST, elimina y redirige a notes_list.
    - Si es GET, muestra un template de confirmación antes de borrar.
    """
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('notes_list')

    return render(request, 'notes_app/note_confirm_delete.html', {'note': note})


# Notes position

@login_required
def update_note_position(request):
    """
    Endpoint que recibe POST JSON con:
      - note_id: ID de la nota a actualizar.
      - pos_x: coordenada X (izquierda) en píxeles.
      - pos_y: coordenada Y (arriba) en píxeles.
    Sólo el propietario de la nota puede actualizarla.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido, use POST.")

    try:
        # Convertimos el body a JSON
        data = json.loads(request.body)
        note_id = data.get('note_id')
        pos_x = int(data.get('pos_x'))
        pos_y = int(data.get('pos_y'))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("JSON inválido o faltan campos: se requieren note_id, pos_x, pos_y.")

    # Verificamos que la nota exista y pertenezca al usuario autenticado
    try:
        note = Note.objects.get(pk=note_id, user=request.user)
    except Note.DoesNotExist:
        return HttpResponseForbidden("No tienes permiso para mover esta nota o la nota no existe.")

    # Actualizamos la posición y guardamos
    note.pos_x = pos_x
    note.pos_y = pos_y
    note.save(update_fields=['pos_x', 'pos_y'])

    return JsonResponse({'status': 'ok'})
