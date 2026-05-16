[app]
title = ProSessionBrowser
package.name = prosession
package.domain = org.privacy

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# Pyjnius diperlukan untuk memanggil API Android Webkit
requirements = python3,kivy,pyjnius

# Wajib: Izin internet untuk memuat halaman web
android.permissions = INTERNET

orientation = portrait
android.archs = arm64-v8a, armeabi-v7a
android.api = 33

[buildozer]
log_level = 2
warn_on_root = 1
