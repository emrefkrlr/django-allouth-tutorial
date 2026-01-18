from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile  # Profile modelini import ettiğinden emin ol

@login_required
def profile(request):
    # Kilit Nokta: Eğer Google veya manuel kayıt sonrası profil oluşmadıysa 
    # bu satır profili otomatik oluşturur ve hatayı engeller.
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Hesabınız başarıyla güncellendi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        # Template içinde profil resmine kolay ulaşmak için objeyi de gönderelim
        'profile': profile_obj 
    }
    return render(request, 'user_profile/profile.html', context)