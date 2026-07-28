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

EN
# Stretched

A simple, fast "stretched" resolution switcher (e.g. 1440×1080 on a 16:9 monitor) for gamers — works with any game that uses Windows screen resolution.

Author: szachowyy

## What it does

- Switches screen resolution with one click or a keyboard shortcut
- Several ready-made "stretched" resolutions to choose from (1440×1080, 1280×1024, 1280×960, 1024×768, 800×600)
- Global hotkey on `.` — works even while a game is active, no need to alt-tab to the program
- Live resolution switching — you can switch between resolutions without reverting to native first
- Automatically detects and syncs with the actual system resolution (e.g. when a game resets it on its own during alt-tab)

## What it does NOT do

This program **only** changes the Windows screen resolution through the official Windows API (`ChangeDisplaySettings`). It doesn't read or modify any game's memory, doesn't inject code, and doesn't bypass anticheats. It's the exact same operation you'd do manually in Windows Settings → Display → Resolution.

## Download

Check the [Releases](https://github.com/szachowyy/stretched-resolution-switcher/releases) tab — a ready-to-use `Stretched.exe`, no Python installation required.

> **Note:** the file isn't code-signed (signing costs money), so Windows SmartScreen may show a "Windows protected your PC" warning. Click "More info" → "Run anyway". This is standard behavior for any unsigned .exe and doesn't mean the program is malicious — the source code is fully public in this repo, you can review it yourself.
>
> Programs that use global keyboard shortcuts (the `keyboard` library) are sometimes also falsely flagged by antivirus software — for the same reason keyloggers use it (global keyboard listening). This is a false positive; the code is fully available here for review.

## Running from source

Requirements: Python 3.10+, Windows

```bash
pip install pywin32 keyboard
python stretched.py
```

## In-game settings (CS2)

For stretched resolution to work properly:

1. NVIDIA Control Panel → Adjust desktop size and position → scaling mode: **Full-screen**, perform scaling on: **GPU**
2. In CS2, set the game's resolution to the same one you selected in the program (e.g. 1440×1080)

If you play in **Fullscreen (exclusive)** mode, the resolution may revert to native after alt-tabbing — this is normal Windows behavior for that mode, not a bug in the program. When you return to the game, simply press `.` again.

## License

MIT — see the [LICENSE](https://github.com/szachowyy/stretched-resolution-switcher/blob/main/LICENSE) file. You're free to use and modify it, but please keep the original author credit.
