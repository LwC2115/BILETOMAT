import customtkinter as ctk
import time
from threading import Thread

class AnimacjaPlacenia(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Wybierz płatność", font=("Arial", 60, "bold"))
        self.label.pack(pady=30)

        # Pasek ładowania
        self.progress_bar = ctk.CTkProgressBar(self, width=600)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)  # Ustawienie paska na 0

        # Komunikat
        self.message_label = ctk.CTkLabel(self, text="Wrzuć monety lub zbliż kartę do terminalu", font=("Arial", 45))
        self.message_label.pack(pady=10)

        # Kwota do zapłaty
        self.total_label = ctk.CTkLabel(self, text="Do zapłaty: 0.00 zł", font=("Arial", 36, "bold"))
        self.total_label.pack(pady=10)

        # Ramka na przyciski płatności
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Przyciski płatności
        self.card_payment_button = ctk.CTkButton(
            self.button_frame, text="Zapłać kartą", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("card")
        )
        self.card_payment_button.grid(row=1, column=1, padx=10, pady=90)

        self.cash_payment_button = ctk.CTkButton(
            self.button_frame, text="Zapłać gotówką", width=300, height=70, font=("Arial", 24, "bold"),
            command=lambda: self.process_payment("cash")
        )
        self.cash_payment_button.grid(row=1, column=0, padx=10, pady=90)

    # Przycisk "Wróć"
        self.back_btn = ctk.CTkButton(
            self,
            text="Wróć",
            width=200,
            height=70,
            font=("Arial", 24, "bold"),
            command=self.go_back
        )
        self.back_btn.place(relx=0.05, rely=0.03, anchor="nw")

        # Przycisk "Powrót na stronę główną"
        self.home_btn = ctk.CTkButton(
            self,
            text="Strona Główna",
            width=200,
            height=70,
            font=("Arial", 24, "bold"),
            command=lambda: self.app.show_frame("MainScreen")
        )
        self.home_btn.place(relx=0.95, rely=0.03, anchor="ne")

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
        self.message_label.configure(text="Płatność zakończona!✔\n Prosze poczekać na wydruk biletu")
        self.progress_bar.set(1)
        time.sleep(4)

        # Powrót do ekranu głównego
        self.app.frames["JednorazoweZKM"].should_reset = True  # Ustaw flagę resetu
        self.app.show_frame("MainScreen")

    def disable_buttons(self):
        """Wyłącza przyciski płatności i wróć."""
        self.card_payment_button.configure(state="disabled")
        self.cash_payment_button.configure(state="disabled")
        self.back_btn.configure(state="disabled")
        self.home_btn.configure(state="disabled")

    def enable_buttons(self):
        """Włącza przyciski płatności i wróć."""
        self.card_payment_button.configure(state="normal")
        self.cash_payment_button.configure(state="normal")
        self.back_btn.configure(state="normal")
        self.home_btn.configure(state="normal")

    def go_back(self):
        """Wróć do poprzedniego ekranu."""
        previous_page = self.app.previous_page if hasattr(self.app, "previous_page") else "MainScreen"
        self.app.show_frame(previous_page)

