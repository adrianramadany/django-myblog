# Cara Menambahkan Foto Profil

## Langkah-langkah:

1. **Siapkan foto profil Anda** (format: JPG, PNG, atau WebP)
2. **Rename foto menjadi:** `profile-photo.jpg`
3. **Letakkan foto di folder ini:** `static/images/profile-photo.jpg`
4. **Atau ganti nama file di template:** 
   - Buka file `templates/blog/about.html`
   - Cari baris: `<img src="{% static 'images/profile-photo.jpg' %}"`
   - Ganti `profile-photo.jpg` dengan nama file foto Anda

## Tips:
- Gunakan foto dengan rasio 1:1 (persegi) untuk hasil terbaik
- Ukuran yang disarankan: 300x300 pixel atau lebih besar
- Format yang didukung: JPG, PNG, WebP
- Jika foto tidak muncul, akan otomatis menampilkan icon default

## Contoh nama file yang bisa digunakan:
- `profile-photo.jpg`
- `adrian-photo.png`
- `my-photo.webp` 