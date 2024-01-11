from django import forms

class UploadFilesForm(forms.Form):
    planilla = forms.FileField(label='Selecciona la planilla')  