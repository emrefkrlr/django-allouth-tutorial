from django import forms
from django.contrib.auth.models import User
from .models import Profile

class MyCustomSignupForm(forms.Form):
    # Django'nun bu alanı tanıması için widget'ı RadioSelect olarak bırakıyoruz
    role = forms.ChoiceField(
        choices=(('requester', 'Requester'), ('employee', 'Employee')),
        required=True,
        initial='requester',
        widget=forms.RadioSelect
    )

    def signup(self, request, user):
        user_role = self.cleaned_data.get('role')
        # Sinyal tarafından oluşturulan profili güncelle
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = user_role
        profile.save()
        # Log kontrolü için (Docker loglarında görünmesi gerekir)
        print(f"--- DEBUG: {user.username} için kaydedilen rol: {user_role} ---")



# Diğer formların değişmesine gerek yok, oldukları gibi kalabilirler
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, label="E-Posta Adresi")
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'phone', 'location', 'birth_date', 'website']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }