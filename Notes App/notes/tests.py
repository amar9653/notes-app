from django.test import TestCase, Client
from django.urls import reverse
from .models import Note
from .forms import NoteForm

class NoteModelTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note content."
        )
    
    def test_note_creation(self):
        """Test that a note is created correctly"""
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "This is a test note content.")
        self.assertTrue(self.note.created_at)
    
    def test_note_str_method(self):
        """Test the string representation of the note"""
        self.assertEqual(str(self.note), "Test Note")

class NoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.note = Note.objects.create(
            title="Test Note",
            content="Test content"
        )
    
    def test_note_list_view(self):
        """Test the note list view"""
        response = self.client.get(reverse('notes:note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, "Add New Note")
    
    def test_add_note_post(self):
        """Test adding a note via POST request"""
        response = self.client.post(reverse('notes:note_list'), {
            'title': 'New Test Note',
            'content': 'New test content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Note.objects.filter(title='New Test Note').exists())
    
    def test_delete_note(self):
        """Test deleting a note"""
        note_id = self.note.pk
        response = self.client.post(reverse('notes:delete_note', args=[note_id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Note.objects.filter(pk=note_id).exists())

class NoteFormTest(TestCase):
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Test Title',
            'content': 'Test content for the note.'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_title_form(self):
        """Test form with empty title"""
        form_data = {
            'title': '',
            'content': 'Test content'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_empty_content_form(self):
        """Test form with empty content"""
        form_data = {
            'title': 'Test Title',
            'content': ''
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
