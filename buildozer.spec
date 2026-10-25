[app]

# (str) Tytuł aplikacji (nazwa, którą zobaczysz pod ikoną na telefonie)
title = Konwerter Zdjec

# (str) Nazwa pakietu (musi być unikalna, bez spacji i polskich znaków)
package.name = konwerterzdjec

# (str) Domena pakietu
package.domain = org.eszpan

# (list) Pliki źródłowe do spakowania
source.include_exts = py,png,jpg,kv,atlas

# (str) Ścieżka do kodu źródłowego
source.dir = .

# (str) Główny plik startowy (musi nazywać się main.py!)
source.main_file = main.py

# (list) Wymagania
requirements = python3,kivy,pillow

# (str) Wersja aplikacji
version = 0.1

# (list) Uprawnienia, których aplikacja będzie żądać na Androida
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Orientacja ekranu (portrait = pionowa)
orientation = portrait

# (bool) Czy aplikacja ma być pełnoekranowa
fullscreen = 0

# (str) Obsługiwane architektur systemowe
android.archs = arm64-v8a

[buildozer]

# Poziom logów (2 = dużo informacji, przydatne przy szukaniu błędów)
log_level = 2

# Katalog roboczy
bin_dir = ./bin
