from django import forms
from .models import tasks
class TaskForm(forms.ModelForm):
    class Meta:
        model = tasks
        fields = ['title','description','important']
        widgets ={
            'title':forms.TextInput(attrs={'class':'form-control', 
                                           'placeholder':'Escribe un Titulo'}),
            'description':forms.Textarea(attrs={'class':'form-control', 
                                          'placeholder':'Escribe la descripcion de la tarea'}),
            'important':forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }