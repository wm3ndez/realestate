from django import forms

class PropiedadContactForm(forms.Form):
    nombre = forms.CharField(max_length=40,required=True)
    email = forms.EmailField(required=True)
    mensaje = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        if not self.mensaje:
            raise forms.ValidationError('El mensaje no puede estar en blanco.')
        return self.cleaned_data['mensaje']