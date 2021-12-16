from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm
from .models import *

class CustomerForm(ModelForm):
    介绍 = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['用户']

class GoodForm(ModelForm):
    class Meta:
        model = Good
        fields = '__all__'
        exclude = ['发布人']
