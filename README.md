# Amedspor - Beşiktaş Bilet Takip Botu

Bu, bilet SATIN ALMAZ. Sadece Passo'da "Amed" ve "Beşiktaş" birlikte geçen
bir etkinlik göründüğünde Telegram'dan sana haber verir. İki farklı yöntemi
aynı anda dener (DuckDuckGo arama + Passo'nun kendi arama sayfası),
hangisi önce bulursa ondan bildirim gelir.

## Kurulum (5 adım)

### 1) GitHub'da yeni bir repo oluştur
- github.com → sağ üstte "+" → "New repository"
- İster public ister private olsun (public'te Actions dakika limiti yok,
  önerilir). Repo adı ne olursa olur.

### 2) Bu klasördeki dosyaları repoya yükle
Bu klasördeki her şeyi (monitor.py, state.json, .github/ klasörü, README.md)
olduğu gibi repona yükle. En kolayı: GitHub'da "Add file" → "Upload files"
ile hepsini sürükle bırak (gizli `.github` klasörünü de dahil et).

### 3) Telegram bilgilerini "Secret" olarak ekle
Repo sayfasında:
- Settings → Secrets and variables → Actions → "New repository secret"
- Şunları ekle:
  - `TELEGRAM_TOKEN` → botunun token'ı (BotFather'dan aldığın)
  - `TELEGRAM_CHAT_ID` → senin chat ID'n

Bunlar kod içinde açıkta durmaz, sadece workflow çalışırken kullanılır.

### 4) Actions'ı etkinleştir
Repo sayfasında "Actions" sekmesine gir, workflow'u ("Bilet Takip") gör,
gerekiyorsa "Enable" de.

### 5) Test et
Actions sekmesinde "Bilet Takip" workflow'unu seç → "Run workflow" ile
elle bir kere çalıştır. Loglardan "Henüz bulunamadı." yazısını görmen,
her şeyin doğru kurulduğu anlamına gelir. Bulunduğunda Telegram'a otomatik
mesaj gelecek.

## Notlar
- Kontrol aralığı 15 dakikada bir (workflow dosyasında değiştirebilirsin).
  GitHub'ın zamanlanmış görevleri bazen birkaç dakika gecikmeli çalışır,
  bu normal.
- Bir kere bulununca `state.json` güncellenip tekrar bildirim gitmesi
  engellenir. Yeniden başlatmak istersen `state.json` içindeki
  `"found": false` yap.
- Bu araç herhangi bir satın alma işlemi yapmaz, sadece herkese açık
  arama sonuçlarını okur.
