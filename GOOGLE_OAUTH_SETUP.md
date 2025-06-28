# Setup Google OAuth untuk MyBlog

## Langkah-langkah Setup Google OAuth:

### 1. Buat Google Cloud Project
1. Kunjungi [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru atau pilih project yang sudah ada
3. Aktifkan Google+ API

### 2. Buat OAuth 2.0 Credentials
1. Buka menu "APIs & Services" > "Credentials"
2. Klik "Create Credentials" > "OAuth 2.0 Client IDs"
3. Pilih "Web application"
4. Isi form:
   - Name: MyBlog OAuth
   - Authorized JavaScript origins: `http://localhost:8000`
   - Authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`
5. Klik "Create"

### 3. Dapatkan Client ID dan Secret
Setelah credentials dibuat, Anda akan mendapatkan:
- Client ID
- Client Secret

### 4. Setup di Django Admin
1. Login ke Django admin: `http://localhost:8000/admin/`
2. Buka "Sites" dan edit site dengan domain `localhost:8000`
3. Buka "Social Applications" dan tambahkan aplikasi baru:
   - Provider: Google
   - Name: Google OAuth
   - Client ID: [Client ID dari Google]
   - Secret Key: [Client Secret dari Google]
   - Sites: Pilih site yang sudah dibuat

### 5. Untuk Production
Untuk deployment di production, ganti URL di Google Console:
- Authorized JavaScript origins: `https://yourdomain.com`
- Authorized redirect URIs: `https://yourdomain.com/accounts/google/login/callback/`

### 6. Test
1. Jalankan server: `python manage.py runserver`
2. Kunjungi: `http://localhost:8000/accounts/login/`
3. Coba login dengan Google

## Troubleshooting
- Pastikan Google+ API sudah diaktifkan
- Periksa URL redirect sudah benar
- Pastikan domain di Django Sites sudah sesuai
- Cek error log di Google Cloud Console 