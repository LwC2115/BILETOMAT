import customtkinter as ctk
import time
from threading import Thread

class AnimacjaPlacenia(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Płatność w toku...", font=("Arial", 36, "bold"))
        self.label.pack(pady=20)

        # Pasek ładowania
        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)  # Ustawienie paska na 0

        # Komunikat
        self.message_label = ctk.CTkLabel(self, text="Wrzuć monety lub zbliż kartę do terminalu", font=("Arial", 24))
        self.message_label.pack(pady=10)

        # Kwota do zapłaty
        self.total_label = ctk.CTkLabel(self, text="Do zapłaty: 0.00 zł", font=("Arial", 24, "bold"))
        self.total_label.pack(pady=10)

        # Przyciski płatności
        self.card_payment_button = ctk.CTkButton(
            self, text="Zapłać kartą", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("card")
        )
        self.card_payment_button.pack(pady=10)

        self.cash_payment_button = ctk.CTkButton(
            self, text="Zapłać gotówką", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("cash")
        )
        self.cash_payment_button.pack(pady=10)

        # Przycisk Wróć
        self.back_btn = ctk.CTkButton(
            self, text="Wróć", width=200, height=50, font=("Arial", 24),
            command=self.go_back
        )
        self.back_btn.pack(pady=20)

    def update_content(self, total_price):
        """Aktualizuje ekran płatności z kwotą do zapłaty."""
        self.total_label.configure(text=f"Do zapłaty: {total_price:.2f} zł")
        self.progress_bar.set(0)  # Resetuj pasek ładowania
        self.message_label.configure(text="Wrzuć monety lub zbliż kartę do terminalu")
        self.enable_buttons()

    def process_payment(self, method):
        """Symuluje proces płatności."""
        self.disable_buttons()
        self.message_label.configure(text=f"Płatność {'kartą' if method == 'card' else 'gotówką'} w toku...")
        Thread(target=self.run_payment_animation).start()

    def run_payment_animation(self):
        """Symulacja animacji płatności."""
        self.message_label.configure(text="Przetwarzanie płatności...")
        for i in range(100):
            self.progress_bar.set(i / 100)
            time.sleep(0.02)

        # Płatność zakończona
        self.message_label.configure(text="Płatność zakończona. Dziękujemy!")
        self.progress_bar.set(1)
        time.sleep(2)

        # Powrót do ekranu głównego
        self.app.frames["JednorazoweZKM"].should_reset = True  # Ustaw flagę resetu
        self.app.show_frame("MainScreen")

    def disable_buttons(self):
        """Wyłącza przyciski płatności i wróć."""
        self.card_payment_button.configure(state="disabled")
        self.cash_payment_button.configure(state="disabled")
        self.back_btn.configure(state="disabled")

    def enable_buttons(self):
        """Włącza przyciski płatności i wróć."""
        self.card_payment_button.configure(state="normal")
        self.cash_payment_button.configure(state="normal")
        self.back_btn.configure(state="normal")

    def go_back(self):
        """Wróć do poprzedniego ekranu."""
        previous_page = self.app.previous_page if hasattr(self.app, "previous_page") else "MainScreen"
        self.app.show_frame(previous_page)

