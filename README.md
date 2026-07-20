# Stretched

Prosty, szybki przełącznik rozdzielczości "stretched" (np. 1440×1080 na monitorze 16:9) dla graczy —  działa z każdą grą korzystającą z rozdzielczości ekranu Windows.

Autor: **szachowyy**

![status](https://img.shields.io/badge/platform-Windows-blue) ![license](https://img.shields.io/badge/license-MIT-green)

## Co to robi

- Przełącza rozdzielczość ekranu jednym kliknięciem lub skrótem klawiszowym
- Kilka gotowych rozdzielczości "stretched" do wyboru (1440×1080, 1280×1024, 1280×960, 1024×768, 800×600)
- Globalny bind na klawisz `.` — działa nawet gdy gra jest aktywna, nie trzeba alt-tabować do programu
- Zmiana rozdzielczości "w locie" — możesz przełączać między rozdzielczościami bez wracania do natywnej
- Automatycznie wykrywa i synchronizuje się z rzeczywistą rozdzielczością systemu (np. gdy gra sama ją zresetuje przy alt-tabie)

## Czego to NIE robi

Ten program **wyłącznie zmienia rozdzielczość ekranu Windows** przez oficjalne Windows API (`ChangeDisplaySettings`). Nie czyta ani nie modyfikuje pamięci żadnej gry, nie wstrzykuje kodu, nie omija anticheatów. To dokładnie ta sama operacja, którą robisz ręcznie w Ustawieniach Windows → Ekran → Rozdzielczość.

## Pobieranie

Zobacz zakładkę **[Releases](../../releases)** — gotowy `Stretched.exe`, nie wymaga instalacji Pythona.

> **Uwaga:** plik nie jest podpisany cyfrowo (podpisanie kosztuje), więc Windows SmartScreen może pokazać ostrzeżenie "Windows chronił Twój komputer". Kliknij "Więcej informacji" → "Uruchom mimo to". To standardowe zachowanie dla każdego niepodpisanego .exe, nie oznacza że program jest szkodliwy — kod źródłowy jest w pełni jawny w tym repo, możesz go przejrzeć sam.
>
> Programy korzystające z globalnych skrótów klawiszowych (biblioteka `keyboard`) czasem są też fałszywie wykrywane przez antywirusy — z tego samego powodu, z którego korzystają keyloggery (globalny nasłuch klawiatury). To fałszywy alarm; kod jest tutaj w całości do wglądu.

## Uruchamianie ze źródła

Wymagania: Python 3.10+, Windows

```bash
pip install pywin32 keyboard
python stretched.py
```

## Ustawienia w grze (CS2)

Żeby stretched resolution działał poprawnie:

1. NVIDIA Control Panel → Dostosuj rozmiar i pozycję pulpitu → tryb skalowania: **Pełny ekran**, wykonaj skalowanie na: **GPU**
2. W CS2 ustaw rozdzielczość gry na tę samą, którą wybrałeś w programie (np. 1440×1080)

Jeśli grasz w trybie **Pełny ekran (exclusive)**, rozdzielczość może wrócić do natywnej po alt-tabie — to normalne zachowanie Windows przy tym trybie, nie błąd programu. Po powrocie do gry po prostu naciśnij `.` ponownie.

## Licencja

MIT — zobacz plik [LICENSE](LICENSE). Możesz swobodnie używać i modyfikować, ale zostaw informację o oryginalnym autorze.
