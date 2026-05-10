[app]
# Judul aplikasi
title = ProKalkulator

# Nama paket (tidak boleh ada spasi atau karakter khusus)
package.name = prokalkulator

# Domain paket (bebas)
package.domain = org.test

# Direktori source code (di mana main.py berada)
source.dir = .

# Ekstensi file yang akan dimasukkan ke APK
source.include_exts = py,png,jpg,kv,atlas

# Versi aplikasi
version = 1.0

# Requirements (Library yang dibutuhkan)
requirements = python3,kivy

# Orientasi layar (portrait atau landscape)
orientation = portrait

# (Opsional) Mengaktifkan presplash/icon jika kamu punya filenya
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png

# Mendukung arsitektur modern untuk Android
android.archs = arm64-v8a, armeabi-v7a

# Versi API Android (sesuaikan dengan target, 31 atau 33 disarankan)
android.api = 33

[buildozer]
# Level log (2 untuk info, 1 untuk warning)
log_level = 2
warn_on_root = 1
