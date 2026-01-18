from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Hakkımda")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    location = models.CharField(max_length=100, blank=True, verbose_name="Konum")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")
    website = models.URLField(blank=True, verbose_name="Web Sitesi")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name="Profil Resmi")

    def __str__(self):
        return f'{self.user.username} Profili'

    @property
    def avatar_url(self):
        # 1. Kullanıcı kendi resmini yüklediyse onu göster
        if self.image and self.image.url != '/media/default.jpg' and self.image.url != '/media/profile_pics/default.jpg':
            return self.image.url
        
        # 2. Google ile bağlandıysa Google profil resmini çek
        # (allauth socialaccount_set üzerinden)
        if self.user.socialaccount_set.exists():
            social_account = self.user.socialaccount_set.filter(provider='google').first()
            if social_account and 'picture' in social_account.extra_data:
                return social_account.extra_data.get('picture')
            
        # 3. Hiçbiri yoksa varsayılan resim
        return "/media/default.jpg"

# Sinyaller: Kullanıcı oluştuğunda otomatik profil oluşturur
@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        # Profil oluşturulurken Google'dan gelen isim/soyisim bilgilerini de 
        # User modeline yazmak için burayı kullanabiliriz.
        Profile.objects.get_or_create(user=instance)
    
    # Profil zaten varsa sadece kaydet (Güncellemeler için)
    if hasattr(instance, 'profile'):
        instance.profile.save()