from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile  # Profile modelini import ettiğinden emin ol

@login_required
def profile(request):
    # Veritabanındaki güncel profil nesnesini alıyoruz
    profile_obj = request.user.profile 

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        
        if u_form.is_valid() and p_form.is_valid():
            # KİLİT NOKTA: Formu kaydetmeden önce rolü bir değişkene sakla
            saved_role = profile_obj.role 
            
            u_form.save()
            # commit=False ile objeyi belleğe alıyoruz
            updated_profile = p_form.save(commit=False)
            # Rolü zorla eski haline (employee) getiriyoruz ki form ezmesin
            updated_profile.role = saved_role
            updated_profile.save()
            
            messages.success(request, f'Hesabınız başarıyla güncellendi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile_obj 
    }
    return render(request, 'user_profile/profile.html', context)