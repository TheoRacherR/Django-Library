from django import forms
from .models import Collection, Genre


class AddBookForm(forms.Form):
    title = forms.CharField(label="Title: ")
    author = forms.CharField(label="Author: ")
    url_image = forms.CharField(label="URL Image: ", empty_value=True)
    publisher = forms.CharField(label="Publisher: ", empty_value=True)
    collection = forms.ModelChoiceField(queryset=Collection.objects.all(),empty_label="Select a choice")
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(),empty_label="Select a choice")
