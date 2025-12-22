from django import forms


class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)