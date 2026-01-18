# Django Allauth Özelleştirilmiş Kayıt ve Profil Sistemi

Bu proje, Django Allauth kullanılarak geliştirilmiş, kullanıcılara kayıt sırasında dinamik rol atayan (Employee/Requester) ve bu rolleri güvenli bir şekilde yöneten bir iskelet yapıdır.

## 🚀 Proje Ne Yapar?
- **Allauth Entegrasyonu:** Standart Django kayıt sürecini e-posta odaklı ve sosyal hesap (Google) destekli hale getirir.
- **Dinamik Rol Seçimi:** Kayıt sırasında şık, ikonlu radyo butonları ile kullanıcı tipi belirlenir.
- **Güvenli Profil Yönetimi:** Kayıt sonrası form verilerinin veritabanına doğru işlenmesini ve güncellemeler sırasında "veri ezilme" (data overriding) sorunlarını önler.

## 🛠 Teknik Uygulama Adımları

### 1. Allauth ve Ayarlar (Settings.py)
Allauth'un çalışması için gerekli temel konfigürasyonlar:
```python
INSTALLED_APPS = [
    ...
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'user_profile', # Profil modelimizin olduğu app
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# Özel formumuzu Allauth'a tanıtıyoruz
ACCOUNT_FORMS = {'signup': 'user_profile.forms.MyCustomSignupForm'}
```

### 2. Kayıt Süreci ve forms.py

Allauth'un standart formuna role alanını eklemek için forms.Form kullandık.

- Neden signup metodu? Allauth, kayıt başarılı olduğunda bu metodu tetikler. Biz de burada kullanıcının seçtiği rolü Profile modeline kaydettik.

### 3. Görsel Arayüz ve JavaScript Köprüsü (signup.html)

Bootstrap radyo butonlarını manuel tasarladığımız için Django'nun bu veriyi tanıması gerekiyordu:

- **Çözüm:** Django'nun asıl form alanını display:none ile gizledik. Kullanıcı bizim şık butonlarımıza tıkladığında, küçük bir JavaScript kodu arka plandaki gizli gerçek inputu güncelledi.

### ⚠️ Kritik Sorun: "Neden Hep Requester Görünüyordu?"
Bu projenin en öğretici kısmı burasıydı. Loglarda "employee" yazmasına rağmen ekranda "requester" görmemizin iki ana sebebi vardı:

### Sorun 1: View Katmanındaki Veri Ezilmesi
profile view fonksiyonu içindeki ProfileUpdateForm, içerisinde role alanını barındırmıyordu. Formu p_form.save() diyerek kaydettiğimizde, Django formda olmayan alanları modeldeki default değerine çekmeye çalışabiliyordu.

### Sorun 2: Sinyal (Signal) Davranışı
post_save sinyali her User kaydedildiğinde çalışıyordu. Eğer sinyal içinde kontrolsüz bir .save() işlemi varsa, formdan gelen güncel veriyi varsayılan değerle eziyordu.


### 🛠 Nasıl Çözdük? (The Fix)

#### View Tarafında Veri Koruma:
views.py içerisinde veriyi kaydetmeden önce mevcut rolü bir değişkene aldık ve form kaydedilirken bu değeri manuel olarak geri yükledik:
```python
current_role = profile_obj.role 
profile = p_form.save(commit=False)
profile.role = current_role # Rolü zorla koruyoruz
profile.save()
```

### Model Tarafında Sinyal Optimizasyonu:

models.py içindeki sinyali sadece profil yoksa oluşturacak şekilde (get_or_create) güncelledik ve gereksiz .save() çağrılarını sildik.

### 📖 Öğrenilen Dersler
- Log vs Görüntü: Loglarda veri doğruysa ama sayfada yanlışsa, veri "render" edilmeden hemen önceki bir adımda (view veya signal) değişiyordur.

- Commit=False: Formda olmayan bir alanı korumak istiyorsanız p_form.save(commit=False) en güvenli dostunuzdur.

- JS Köprüsü: Manuel HTML form elemanları kullanıyorsanız, Django'nun cleaned_data mekanizmasına JavaScript ile veri pompalamanız gerekebilir.