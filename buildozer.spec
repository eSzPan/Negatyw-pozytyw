[app]

# (str) Tytuł aplikacji (nazwa, którą zobaczysz pod ikoną na telefonie)
title = Konwerter Zdjec

# (str) Nazwa pakietu (musi być unikalna, bez spacji i polskich znaków)
package.name = konwerterzdjec

# (str) Domena pakietu
package.domain = org.eszpan

# (list) Pliki źródłowe do spakowania (zostaw domyślnie, weźmie wszystko z folderu)
source.include_exts = py,png,jpg,kv,atlas

# (str) Główny plik startowy (musi nazywać się main.py!)
source.main_file = main.py

# (list) Wymagania – TUTAJ WPISUJESZ BIBLIOTECZKI Z KTÓRYCH KORZYSTASZ!
# Dla Kivy i Pillow wpisz dokładnie to:
requirements = python3,kivy,pillow

# (str) Wersja aplikacji
version = 0.1

# (list) Uprawnienia, których aplikacja będzie żądać na Androida 
# (ponieważ konwertujesz zdjęcia, potrzebny będzie dostęp do pamięci/odczyt/zapis):
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Orientacja ekranu (portrait = pionowa, landscape = pozioma, all = obracana)
orientation = portrait

# (bool) Czy aplikacja ma być pełnoekranowa
fullscreen = 0

# (str) Obsługiwane architektur systemowe (arm64-v8a to standard dla współczesnych telefonów)
android.archs = arm64-v8a

[buildozer]

# Poziom logów (2 = dużo informacji, przydatne przy szukaniu błędów)
log_level = 2

# Katalog roboczy
bin_dir = ./bin

[app]

# (str) Tytuł aplikacji (nazwa, którą zobaczysz pod ikoną na telefonie)
title = Konwerter Zdjec

# (str) Nazwa pakietu (musi być unikalna, bez spacji i polskich znaków)
package.name = konwerterzdjec

# (str) Domena pakietu
package.domain = org.eszpan

# (list) Pliki źródłowe do spakowania (zostaw domyślnie, weźmie wszystko z folderu)
source.include_exts = py,png,jpg,kv,atlas

# (list) Główne pliki aplikacji
source.include_dir = 

# (str) Główny plik startowy (musi nazywać się main.py!)
source.main_file = main.py

# (list) Wymagania – TUTAJ WPISUJESZ BIBLIOTECZKI Z KTÓRYCH KORZYSTASZ!
# Dla Kivy i Pillow wpisz dokładnie to:
requirements = python3,kivy,pillow

# (str) Wersja aplikacji
version = 0.1

# (list) Uprawnienia, których aplikacja będzie żądać na Androida 
# (ponieważ konwertujesz zdjęcia, potrzebny będzie dostęp do pamięci/odczyt/zapis):
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Orientacja ekranu (portrait = pionowa, landscape = pozioma, all = obracana)
orientation = portrait

# (bool) Czy aplikacja ma być pełnoekranowa
fullscreen = 0

# (str) Obsługiwane architektur systemowe (arm64-v8a to standard dla współczesnych telefonów)
android.archs = arm64-v8a

[buildozer]

# Poziom logów (2 = dużo informacji, przydatne przy szukaniu błędów)
log_level = 2

# Katalog roboczy
bin_dir = ./bin

# (str) Path to your source code, relative to the spec file.
source.dir = .


