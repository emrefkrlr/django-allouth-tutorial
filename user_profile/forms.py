from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    # E-posta değiştirilemez, sadece bilgi amaçlı gösterilir
    email = forms.EmailField(disabled=True, label="E-Posta Adresi")

    class Meta:
        model = User
        # Username alanını çıkardık, sadece isim ve soyisim düzenlenebilir
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Ad',
            'last_name': 'Soyad',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'phone', 'location', 'birth_date', 'website']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'image': 'Profil Resmini Değiştir',
            'bio': 'Hakkımda',
            'phone': 'Telefon Numarası',
            'location': 'Şehir/Konum',
            'website': 'Kişisel Websitesi',
        }