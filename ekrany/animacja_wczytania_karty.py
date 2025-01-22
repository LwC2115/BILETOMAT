import customtkinter as ctk
import time
from threading import Thread

class AnimacjaWczytaniaKarty(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Wczytaj karte", font=("Arial", 36, "bold"))
        self.label.pack(pady=20)

        # Pasek ładowania
        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)  # Ustawienie paska na 0

        # Komunikat
        self.message_label = ctk.CTkLabel(self, text="Zbliż swoją karte miejską", font=("Arial", 24))
        self.message_label.pack(pady=10)

        # Ramka na przyciski płatności
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Przyciski płatności w wierszu
        self.karta_ulgowa_button = ctk.CTkButton(
            self.button_frame, text="Karta ulgowa imienna", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("ulgowy", "OkresowyUlgowy_1")
        )
        self.karta_ulgowa_button.grid(row=1, column=0, padx=10, pady=90)

        self.karta_normalna_button = ctk.CTkButton(
            self.button_frame, text="Karta normalna imienna", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("normalny", "OkresowyNormalny")
        )
        self.karta_normalna_button.grid(row=1, column=1, padx=10, pady=90)

        self.karta_NaOkaziciela_button = ctk.CTkButton(
            self.button_frame, text="Karta na okaziciela", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("okaziciel", "OkresowyOkaziciela")
        )
        self.karta_NaOkaziciela_button.grid(row=1, column=2, padx=10, pady=90)

        # Przycisk Wróć
        self.back_btn = ctk.CTkButton(
            self, text="Wróć", width=200, height=50, font=("Arial", 24),
            command=self.go_back
        )
        self.back_btn.pack(pady=20)

    def update_content(self):
        """Aktualizuje ekran płatności z kwotą do zapłaty."""
        self.progress_bar.set(0)  # Resetuj pasek ładowania
        self.message_label.configure(text="Zbliż swoją karte miejską")
        self.enable_buttons()

    def process_payment(self,method, next_screen):
        """Symuluje proces płatności."""
        self.disable_buttons()
        self.message_label.configure(text=f"Wczytywanie karty w toku...")
        Thread(target=self.run_payment_animation, args=(next_screen,)).start()

    def run_payment_animation(self, next_screen):
        """Symulacja animacji płatności."""
        # Symulacja procesu płatności
        self.message_label.configure(text="Przetwarzanie karty...")
        for i in range(100):
            self.progress_bar.set(i / 100)
            time.sleep(0.02)

        # Płatność zakończona
        self.message_label.configure(text="Karta wczytana!")
        self.progress_bar.set(1)
        time.sleep(0.5)
        # Przejście do odpowiedniego ekranu
        if(next_screen=="OkresowyUlgowy_1"):
            self.app.show_frame("OkresowyUlgowy_1")
        else:
            self.app.show_frame("Wybor_Rejonu",next_screen)

    def disable_buttons(self):
        """Wyłącza przyciski płatności i wróć."""
        self.karta_normalna_button.configure(state="disabled")
        self.karta_ulgowa_button.configure(state="disabled")
        self.karta_NaOkaziciela_button.configure(state="disabled")
        self.back_btn.configure(state="disabled")

    def enable_buttons(self):
        """Włącza przyciski płatności i wróć."""
        self.karta_normalna_button.configure(state="normal")
        self.karta_ulgowa_button.configure(state="normal")
        self.karta_NaOkaziciela_button.configure(state="normal")
        self.back_btn.configure(state="normal")

    def go_back(self):
        """Wróć do poprzedniego ekranu."""
        self.app.show_frame("MainScreen")
