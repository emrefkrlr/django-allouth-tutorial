# Python'un resmi hafif sürümünü kullanıyoruz
FROM python:3.12-slim

# Terminal çıktılarını anlık görebilmek için
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Çalışma klasörünü oluştur
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . /app/