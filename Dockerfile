# Python 3.13 resmi imajını temel alıyoruz
FROM python:3.13-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gerekli dosyaları kopyalıyoruz
COPY requirements.txt .

# Bağımlılıkları yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalıyoruz
COPY . .

# Uygulamayı başlatma komutu
CMD ["python", "-m", "src.main"]
