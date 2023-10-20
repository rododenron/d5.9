from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = ['subject', 'author', 'text', 'rating']
       
    def clean(self):
       cleaned_data = super().clean()
