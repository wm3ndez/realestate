from django import forms

class PropiedadContactForm(forms.Form):
    nombre = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(required=False)
    mensaje = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(PropiedadContactForm, self).clean()
        if not cleaned_data.get('mensaje'):
            raise forms.ValidationError('El mensaje no puede estar en blanco.')
        return cleaned_data