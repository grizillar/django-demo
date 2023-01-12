from django import forms


class UploadFileForm(forms.Form):
    csvfile = forms.FileField()
