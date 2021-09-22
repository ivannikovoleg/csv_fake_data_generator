from django import forms

class GenerateSchema(forms.Form):
    schema_name = forms.CharField(max_length=200)
