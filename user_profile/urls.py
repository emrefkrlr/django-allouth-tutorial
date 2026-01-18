from django.urls import path
from .views import profile

urlpatterns = [
    # domain.com/profile/ adresine gidince bu view çalışır
    path('', profile, name='profile'),
]