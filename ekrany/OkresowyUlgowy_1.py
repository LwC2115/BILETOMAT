import customtkinter as ctk


class OkresowyUlgowy_1(ctk.CTkFrame):
    def __init__(self, app, selected_language):
        super().__init__(app)
        self.app = app
        self.selected_bilet = None  # Zmienna do przechowywania wybranego biletu
        self.selected_button = None  # Zmienna do przechowywania aktualnie wybranego przycisku

        self.bilety = [
            {"nazwa": "Miesięczny"},
            {"nazwa": "Semestralny 4-miesięczny"},
            {"nazwa": "Semestralny 5-miesięczny"},
        ]

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Bilet okresowy ZKM w Gdyni", font=("Arial", 40, "bold"))
        self.label.pack(pady=20)

        # Ramka dla przycisków głównych
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=5, padx=20, fill="both", expand=True)

        # Powiększone przyciski główne dla każdego biletu
        self.buttons = []
        for i, bilet in enumerate(self.bilety):
            row, col = divmod(i, 2)  # Oblicz rząd i kolumnę
            button = ctk.CTkButton(
                button_frame,
                text=bilet["nazwa"],
                width=400,
                height=150,
                font=("Arial", 30, "bold"),
            )
            # Ustawienie komendy po utworzeniu przycisku
            button.configure(command=lambda b=bilet, btn=button: self.select_bilet(b, btn))
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.buttons.append(button)

        # Rozciąganie kolumn w siatce
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Dodanie przycisku "Zapłać" na końcu siatki
        self.pay_button = ctk.CTkButton(
            button_frame,
            text="Wybierz rodzaj",
            font=("Arial", 30, "bold"),
            height=70,
            width=300,
            state="disabled",  # Domyślnie wyłączony
            command=self.go_next
        )
        self.pay_button.grid(row=2, column=1,  padx=10, pady=20)

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

    def select_bilet(self, bilet, button):
        """Obsługuje wybór biletu i zmienia kolor wybranego przycisku."""
        # Ustaw wybrany bilet
        self.selected_bilet = bilet

        # Zresetuj kolor dla poprzednio wybranego przycisku
        if self.selected_button:
            self.selected_button.configure(fg_color="#3b8ed0")  # Przywróć domyślny styl

        # Ustaw nowy wybrany przycisk i zmień jego kolor
        self.selected_button = button
        self.selected_button.configure(fg_color="#003366")  # Kolor podświetlenia

        # Zaktualizuj tekst przycisku "Zapłać"
        self.pay_button.configure(text=f"Dalej", state="normal")

    
    def go_next(self):
        """Rozpocznij płatność."""
        if self.selected_bilet is not None: 
                rodzaj = self.selected_bilet["nazwa"]
                self.app.show_frame("Wybor_Rejonu", rodzaj)

    def go_back(self):
        """Akcja przycisku 'Wróć'."""
        self.app.show_frame("MainScreen")

    def on_enter(self, previous_page=None, *args):
        """Resetuje stan ekranu przy wejściu."""
        self.selected_bilet = None
        self.selected_button = None
        self.pay_button.configure(text="Wybierz rodzaj ", state="disabled")
        for button in self.buttons:
            button.configure(fg_color="#3b8ed0")  # Przywróć domyślny kolor