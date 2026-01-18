from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('requester', 'Requester'),
        ('employee', 'Employee'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='requester', verbose_name="Kullanıcı Rolü")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Hakkımda")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    location = models.CharField(max_length=100, blank=True, verbose_name="Konum")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")
    website = models.URLField(blank=True, verbose_name="Web Sitesi")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name="Profil Resmi")

    def __str__(self):
        return f'{self.user.username} Profili'

    def get_role_theme(self):
        """Rolün rengini ve ikonunu döndürür"""
        if self.role == 'employee':
            return {'color': 'success', 'icon': 'bi-briefcase'}
        return {'color': 'info', 'icon': 'bi-person-up'}

    @property
    def avatar_url(self):
        if self.image and self.image.url != '/media/default.jpg' and self.image.url != '/media/profile_pics/default.jpg':
            return self.image.url
        
        if self.user.socialaccount_set.exists():
            social_account = self.user.socialaccount_set.filter(provider='google').first()
            if social_account and 'picture' in social_account.extra_data:
                return social_account.extra_data.get('picture')
            
        return "/media/default.jpg"
    
@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        # Sadece yoksa oluşturur, varsa hiçbir şeyi değiştirmez
        Profile.objects.get_or_create(user=instance)
    # DİKKAT: Burada instance.profile.save() satırı varsa MUTLAKA SİLİN.