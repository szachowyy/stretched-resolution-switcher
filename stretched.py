"""
Stretched — szybkie przełączanie rozdzielczości stretched (Windows).

Autor: szachowyy
Licencja: MIT — zobacz plik LICENSE w repozytorium.

Wymagania:
    pip install pywin32 keyboard

Funkcje:
    - Wybór jednej z kilku popularnych rozdzielczości "stretched"
    - Przełączanie przyciskiem w oknie programu
    - Globalny bind na klawisz "." (działa nawet gdy gra jest aktywna)
    - Zmiana rozdzielczości "w locie" nawet gdy tryb stretched jest już aktywny
"""

import ctypes
import tkinter as tk
from tkinter import messagebox

try:
    import win32api
    import win32con
except ImportError:
    win32api = None
    win32con = None

try:
    import keyboard
except ImportError:
    keyboard = None


# ---------------------------------------------------------------- KONFIG ---

RESOLUTIONS = [
    ("1440 x 1080", 1440, 1080),
    ("1280 x 1024", 1280, 1024),
    ("1280 x 960", 1280, 960),
    ("1024 x 768", 1024, 768),
    ("800 x 600", 800, 600),
]

HOTKEY = "."

# Paleta — czarny, czytelny dark UI
BG = "#000000"
CARD = "#131318"
CARD_BORDER = "#2a2a32"
ACCENT = "#6366f1"
ACCENT_HOVER = "#7c7ff5"
ACCENT_SOFT = "#20213a"
TEXT_MAIN = "#f5f5f7"
TEXT_MUTED = "#84848f"
GREEN = "#30d158"
ORANGE = "#ff9f0a"


# ------------------------------------------------------------- LOGIKA OS ---

def get_current_resolution():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def change_resolution(width, height):
    if win32api is None:
        messagebox.showerror(
            "Brak modułu",
            "Musisz zainstalować pywin32:\n\npip install pywin32",
        )
        return False

    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    result = win32api.ChangeDisplaySettings(devmode, 0)
    if result == win32con.DISP_CHANGE_SUCCESSFUL:
        return True

    messagebox.showerror(
        "Błąd",
        f"Nie udało się zmienić rozdzielczości (kod błędu: {result}).\n"
        "Ten monitor może nie obsługiwać podanej rozdzielczości.",
    )
    return False


# -------------------------------------------------------------- WIDGETY ----

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=344, height=56,
                 bg=ACCENT, hover_bg=ACCENT_HOVER, fg=TEXT_MAIN, radius=16,
                 font=("Segoe UI", 12, "bold"), parent_bg=BG):
        super().__init__(parent, width=width, height=height, bg=parent_bg,
                          highlightthickness=0, bd=0)
        self.command = command
        self.bg_color = bg
        self.hover_color = hover_bg
        self.fg = fg
        self.radius = radius
        self.w = width
        self.h = height
        self.font = font
        self.enabled = True
        self.text = text

        self._draw(bg)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(2, 2, self.w - 2, self.h - 2, self.radius, fill=color, outline="")
        self.create_text(self.w / 2, self.h / 2, text=self.text, fill=self.fg, font=self.font)

    def _on_click(self, _e):
        if self.enabled and self.command:
            self.command()

    def _on_enter(self, _e):
        if self.enabled:
            self._draw(self.hover_color)
            self.config(cursor="hand2")

    def _on_leave(self, _e):
        if self.enabled:
            self._draw(self.bg_color)

    def set_text(self, text):
        self.text = text
        self._draw(self.bg_color if self.enabled else "#33384a")

    def set_enabled(self, enabled):
        self.enabled = enabled
        self._draw(self.bg_color if enabled else "#33384a")


class ResChip(tk.Canvas):
    """Klikalny chip wyboru rozdzielczości."""

    def __init__(self, parent, label, on_click, width=163, height=44, selected=False):
        super().__init__(parent, width=width, height=height, bg=BG,
                          highlightthickness=0, bd=0)
        self.label = label
        self.on_click = on_click
        self.selected = selected
        self.w = width
        self.h = height
        self._draw()
        self.bind("<Button-1>", lambda e: self.on_click())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self, hover=False):
        self.delete("all")
        if self.selected:
            fill, outline, fg = ACCENT_SOFT, ACCENT, TEXT_MAIN
        elif hover:
            fill, outline, fg = "#1c1c22", CARD_BORDER, TEXT_MAIN
        else:
            fill, outline, fg = CARD, CARD_BORDER, TEXT_MUTED
        self._round_rect(1, 1, self.w - 1, self.h - 1, 12, fill=fill, outline=outline, width=1.4)
        self.create_text(self.w / 2, self.h / 2, text=self.label, fill=fg, font=("Segoe UI", 10, "bold"))

    def _on_enter(self, _e):
        self.config(cursor="hand2")
        self._draw(hover=True)

    def _on_leave(self, _e):
        self._draw(hover=False)

    def set_selected(self, selected):
        self.selected = selected
        self._draw()


# ----------------------------------------------------------------- APP -----

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Stretched")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.original_resolution = get_current_resolution()
        self.selected_index = 0
        self.is_stretched = False
        self.chips = []

        self._build_ui()
        self._register_hotkey()
        self._poll_resolution()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------------------------------------------------------- UI BUILD --

    def _build_ui(self):
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=28, pady=(28, 6))

        title_row = tk.Frame(top, bg=BG)
        title_row.pack(fill="x")
        tk.Label(title_row, text="Stretched", font=("Segoe UI", 20, "bold"),
                  fg=TEXT_MAIN, bg=BG).pack(side="left")

        badge = tk.Label(title_row, text=f"Bind {HOTKEY.upper()}", font=("Segoe UI", 9, "bold"),
                          fg=ACCENT, bg=ACCENT_SOFT, padx=10, pady=4)
        badge.pack(side="right", pady=4)

        tk.Label(top, text="Szybkie przełączanie rozdzielczości do gier",
                  font=("Segoe UI", 10), fg=TEXT_MUTED, bg=BG).pack(anchor="w", pady=(2, 0))

        # Karta statusu
        card = tk.Frame(self.root, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1)
        card.pack(padx=28, pady=(18, 14), fill="x")
        inner = tk.Frame(card, bg=CARD)
        inner.pack(padx=20, pady=16, fill="x")

        row1 = tk.Frame(inner, bg=CARD)
        row1.pack(fill="x", pady=(0, 10))
        tk.Label(row1, text="Aktualna rozdzielczość", font=("Segoe UI", 9),
                  fg=TEXT_MUTED, bg=CARD).pack(side="left")
        self.current_value = tk.Label(
            row1, text=f"{self.original_resolution[0]} × {self.original_resolution[1]}",
            font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=CARD,
        )
        self.current_value.pack(side="right")

        row2 = tk.Frame(inner, bg=CARD)
        row2.pack(fill="x")
        tk.Label(row2, text="Status", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=CARD).pack(side="left")
        status_frame = tk.Frame(row2, bg=CARD)
        status_frame.pack(side="right")
        self.status_dot = tk.Canvas(status_frame, width=10, height=10, bg=CARD, highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 6))
        self.status_dot.create_oval(1, 1, 9, 9, fill=GREEN, outline="")
        self.status_label = tk.Label(status_frame, text="Natywna", font=("Segoe UI", 10, "bold"),
                                       fg=GREEN, bg=CARD)
        self.status_label.pack(side="left")

        # Wybór rozdzielczości
        tk.Label(self.root, text="Wybierz rozdzielczość stretched",
                  font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG).pack(anchor="w", padx=28, pady=(4, 8))

        note = tk.Label(self.root, text="Możesz zmieniać rozdzielczość na żywo, nawet gdy stretched jest już włączony",
                          font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG, wraplength=340, justify="left")
        note.pack(anchor="w", padx=28, pady=(0, 8))

        grid = tk.Frame(self.root, bg=BG)
        grid.pack(padx=28, fill="x")
        for i, (label, w, h) in enumerate(RESOLUTIONS):
            r, c = divmod(i, 2)
            chip = ResChip(grid, label, on_click=lambda idx=i: self._select_resolution(idx),
                            width=163, height=44, selected=(i == self.selected_index))
            chip.grid(row=r, column=c, padx=(0, 8), pady=(0, 8), sticky="w")
            self.chips.append(chip)

        # Główny przycisk
        btn_wrap = tk.Frame(self.root, bg=BG)
        btn_wrap.pack(pady=(16, 10))
        self.toggle_button = RoundedButton(
            btn_wrap, text=self._target_label(), command=self.toggle_resolution,
            width=344, height=56, parent_bg=BG,
        )
        self.toggle_button.pack()

        hint = "Wciśnij '.' w dowolnym momencie (także w grze), aby przełączyć" if keyboard else \
               "Zainstaluj 'keyboard' (pip install keyboard), aby używać bindu globalnie"
        hint_color = TEXT_MUTED if keyboard else ORANGE
        tk.Label(self.root, text=hint, font=("Segoe UI", 9), fg=hint_color,
                  bg=BG, wraplength=340, justify="center").pack(pady=(0, 6))

        tk.Label(self.root, text="Stretched by szachowyy", font=("Segoe UI", 8),
                  fg="#3f3f47", bg=BG).pack(side="bottom", pady=(0, 10))

    # -------------------------------------------------------------- LOGIC --

    def _target_label(self):
        label, w, h = RESOLUTIONS[self.selected_index]
        return f"Włącz stretched {label}"

    def _select_resolution(self, index):
        self.selected_index = index
        for i, chip in enumerate(self.chips):
            chip.set_selected(i == index)

        if self.is_stretched:
            # zmiana rozdzielczości "w locie" — bez wracania do natywnej
            label, w, h = RESOLUTIONS[index]
            self.toggle_button.set_enabled(False)
            self.root.update_idletasks()
            if change_resolution(w, h):
                self.current_value.config(text=label)
                self.toggle_button.set_text(
                    f"Przywróć {self.original_resolution[0]} × {self.original_resolution[1]}"
                )
            self.toggle_button.set_enabled(True)
        else:
            self.toggle_button.set_text(self._target_label())

    def toggle_resolution(self):
        self.toggle_button.set_enabled(False)
        self.root.update_idletasks()

        if not self.is_stretched:
            label, w, h = RESOLUTIONS[self.selected_index]
            if change_resolution(w, h):
                self.is_stretched = True
                self.toggle_button.set_text(
                    f"Przywróć {self.original_resolution[0]} × {self.original_resolution[1]}"
                )
                self.current_value.config(text=label)
                self._set_status("Stretched", ORANGE)
        else:
            if change_resolution(*self.original_resolution):
                self.is_stretched = False
                self.toggle_button.set_text(self._target_label())
                self.current_value.config(
                    text=f"{self.original_resolution[0]} × {self.original_resolution[1]}"
                )
                self._set_status("Natywna", GREEN)

        self.toggle_button.set_enabled(True)

    def _set_status(self, text, color):
        self.status_label.config(text=text, fg=color)
        self.status_dot.delete("all")
        self.status_dot.create_oval(1, 1, 9, 9, fill=color, outline="")

    # ------------------------------------------------------------ HOTKEY --

    def _register_hotkey(self):
        if keyboard is None:
            return
        try:
            keyboard.add_hotkey(HOTKEY, self._hotkey_callback)
        except Exception:
            pass

    def _hotkey_callback(self):
        self.root.after(0, self.toggle_resolution)

    def _poll_resolution(self):
        """Co sekundę sprawdza rzeczywistą rozdzielczość systemu i synchronizuje UI.
        Wykrywa np. sytuację, gdy gra (CS2) sama zresetuje rozdzielczość
        przy alt-tabie, a program o tym wcześniej nie wiedział."""
        actual = get_current_resolution()
        target_label, tw, th = RESOLUTIONS[self.selected_index]

        if actual == (tw, th) and not self.is_stretched:
            self.is_stretched = True
            self.toggle_button.set_text(
                f"Przywróć {self.original_resolution[0]} × {self.original_resolution[1]}"
            )
            self.current_value.config(text=target_label)
            self._set_status("Stretched", ORANGE)
        elif actual == self.original_resolution and self.is_stretched:
            self.is_stretched = False
            self.toggle_button.set_text(self._target_label())
            self.current_value.config(text=f"{actual[0]} × {actual[1]}")
            self._set_status("Natywna", GREEN)
        elif actual not in (self.original_resolution, (tw, th)):
            # inna, nieoczekiwana rozdzielczość (np. gra ustawiła własną)
            self.current_value.config(text=f"{actual[0]} × {actual[1]}")
            self._set_status("Inna / gra", ORANGE)

        self.root.after(1000, self._poll_resolution)

    def _on_close(self):
        if keyboard is not None:
            try:
                keyboard.unhook_all_hotkeys()
            except Exception:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
