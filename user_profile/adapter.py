from django.shortcuts import resolve_url
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    # Bu metod MANUEL (form ile) kayıt sonrası çalışır
    def get_signup_redirect_url(self, request):
        return resolve_url('profile')

    # Bu metod LOGIN (giriş) sonrası çalışır
    def get_login_redirect_url(self, request):
        user = request.user
        # Eğer kullanıcı hiç giriş yapmadıysa veya yeni kayıt olduysa profile gönder
        if user.last_login is None:
            return resolve_url('profile')
        return resolve_url('/')

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    # Bu metod Google/Sosyal hesap ile İLK KEZ kayıt olunca çalışır
    def get_signup_redirect_url(self, request, sociallogin):
        return resolve_url('profile')

    # Bu metod sosyal hesap bağlandığında veya giriş yapıldığında çalışır
    def get_connect_redirect_url(self, request, socialaccount):
        return resolve_url('profile')