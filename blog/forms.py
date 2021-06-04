from django import forms
from django.db.models import query
from django.forms import fields, models
from .models import Comment



class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder':'Type your comment',
        'id' :'usercomment',
        'rows':4
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder': 'Name',
        'id': 'usercomment',

    }))
    class Meta:
        model = Comment
        fields = ['name', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()
    