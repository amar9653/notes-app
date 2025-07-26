from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Note
from .forms import NoteForm

def note_list(request):
    """Display all notes and handle note creation"""
    notes = Note.objects.all()
    form = NoteForm()
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note added successfully!')
            return redirect('notes:note_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    
    context = {
        'notes': notes,
        'form': form,
    }
    return render(request, 'notes/note_list.html', context)

def add_note(request):
    """Alternative view for adding notes (optional)"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note added successfully!')
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    
    context = {'form': form}
    return render(request, 'notes/note_form.html', context)

def delete_note(request, pk):
    """Delete a note"""
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes:note_list')
    
    # If GET request, show confirmation
    context = {'note': note}
    return render(request, 'notes/note_confirm_delete.html', context)
