from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    '''
    Formulario para enviar un correo electrónico sobre una entrada del blog.
    '''
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    '''
    Formulario para añadir un comentario a una entrada del blog.
    Basado en el modelo Comment.
    '''
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    '''
    Formulario para buscar entradas del blog.
    '''
    query = forms.CharField()