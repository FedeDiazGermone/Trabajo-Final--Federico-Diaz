from django import forms
from .models import Producto, Proveedor, Avatar
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class ProdFormulario(forms.Form):

  class Meta:
    model = Producto
    fields=('__all__')


class ProvFormulario(forms.Form):

  codigo = forms.CharField(max_length=30)
  nombre = forms.CharField(max_length=30)  
  email = forms.EmailField()
  telefono = forms.CharField(max_length=30)    


class CompraFormulario(forms.Form):

  nro = forms.IntegerField()
  fecha_compra = forms.DateField()
  cantidad = forms.IntegerField()  
  precio_venta = forms.FloatField()
  producto = forms.ModelChoiceField(queryset=Producto.objects.all())
  proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all())


class AvatarFormulario(forms.ModelForm):

  class Meta:
    model=Avatar
    fields=('imagen',)
  


class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label="Administrador", initial=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_staff',)


class UserEditForm(UserChangeForm):
    password = forms.CharField(help_text="", widget=forms.HiddenInput(), required=False)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    is_staff = forms.BooleanField(required=False, label="Administrador")

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "is_staff"]

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas deben ser iguales")
        return password2


  