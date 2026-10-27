[app]

# Tytuł aplikacji (nazwa pod ikoną)
title = Konwerter Zdjec

# Nazwa pakietu (bez spacji i polskich znaków)
package.name = konwerterzdjec

# Domena pakietu
package.domain = org.eszpan

# Rozszerzenia plików do spakowania
source.include_exts = py,png,jpg,kv,atlas

# Katalog ze źródłami
source.dir = .

# Główny plik startowy
source.main_file = main.py

# Wymagania (numpy jest potrzebne, bo używasz go w kodzie)
requirements = python3,kivy,pillow,numpy

# Wersja aplikacji
version = 0.1

# Uprawnienia
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Orientacja
orientation = portrait

# Pełny ekran (0 = nie)
fullscreen = 0

# Architektura
android.archs = arm64-v8a

# --- POPRAWKI POD BUDOWĘ ---
android.accept_sdk_license = True
android.skip_update = False
android.build_tools_version = 34.0.0
android.api = 34
android.minapi = 24
android.ndk = 25b

[buildozer]

# Poziom logów
log_level = 2

# Katalog wynikowy
bin_dir = ./bin
