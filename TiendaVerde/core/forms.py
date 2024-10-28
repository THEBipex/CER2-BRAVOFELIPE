from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Order, SolicitudReciclaje

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clases de Bootstrap a todos los campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

class SolicitudReciclajeForm(forms.ModelForm):
    TIPOS_RESIDUOS = [
        ('plastico', 'Plástico'),
        ('papel', 'Papel'),
        ('vidrio', 'Vidrio'),
        ('metales', 'Metales'),
        ('electronicos', 'Electrónicos'),
    ]
    
    SUBCATEGORIAS = {
        'plastico': [('botellas', 'Botellas'), ('envases', 'Envases'), ('bolsas', 'Bolsas')],
        'papel': [('periodicos', 'Periódicos'), ('carton', 'Cartón'), ('papel_oficina', 'Papel de oficina')],
        'vidrio': [('botellas', 'Botellas'), ('frascos', 'Frascos'), ('cristaleria', 'Cristalería')],
        'metales': [('latas', 'Latas'), ('cables', 'Cables'), ('electrodomesticos', 'Electrodomésticos pequeños')],
        'electronicos': [('telefonos', 'Teléfonos móviles'), ('baterias', 'Baterías'), ('componentes', 'Componentes de computadoras')],
    }
    
    tipo_residuo = forms.ChoiceField(
        choices=TIPOS_RESIDUOS,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'tipo-residuo'
        })
    )
    
    subcategoria = forms.ChoiceField(
        choices=[],  # Se poblará dinámicamente con JavaScript
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'subcategoria'
        })
    )
    
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    
    direccion = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección de recolección'
        })
    )
    
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cantidad de residuos'
        })
    )
    
    comentarios = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Comentarios adicionales',
            'rows': 4
        })
    )
    
    class Meta:
        model = SolicitudReciclaje
        fields = ['tipo_residuo', 'subcategoria', 'nombre', 'email', 'direccion', 'cantidad', 'comentarios']

class CarritoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'  # Para esta evaluación solo se permite 1 unidad
        })
    )