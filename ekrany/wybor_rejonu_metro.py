import customtkinter as ctk


class Wybor_Rejonu_Metro(ctk.CTkFrame):
    def __init__(self, app, rodzaj_biletu):
        super().__init__(app)
        self.app = app
        self.selected_bilet = None  # Zmienna do przechowywania wybranego biletu
        self.selected_button = None  # Zmienna do przechowywania aktualnie wybranego przycisku
        self.rodzaj_biletu = rodzaj_biletu  # Rodzaj biletu przekazany z poprzedniego ekranu


        self.bilety = [
            {"nazwa": "Komunalny", "ceny": {"OkresowyNormalny": 156.00, "OkresowyUlgowy_1": 78.00}},
            {"nazwa": "Gdańsk-Sopot albo Gdynia-Sopot", "ceny": {"OkresowyNormalny": 80.00, "OkresowyUlgowy_1": 40.00}},
            {"nazwa": "Sieciowy jednego organizatora", "ceny": {"OkresowyNormalny": 86.00, "OkresowyUlgowy_1": 43.00}},
            {"nazwa": "Na cały obszar MZKZG", "ceny": {"OkresowyNormalny": 106.00, "OkresowyUlgowy_1": 53.00}},
        ]

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Bilety okresowy ZKM w Gdyni", font=("Arial", 40, "bold"))
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
                font=("Arial", 20, "bold"),
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
            text="Zapłać",
            font=("Arial", 30, "bold"),
            height=70,
            width=300,
            state="disabled",  # Domyślnie wyłączony
            command=self.start_payment
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
    
    def on_enter(self, previous_page, rodzaj_biletu):
        """Funkcja wywoływana przy wejściu na ekran."""
        self.rodzaj_biletu = rodzaj_biletu  # Przechowaj przekazany rodzaj biletu
        # Zresetuj stan, jeśli to konieczne
        self.selected_bilet = None
        self.selected_button = None
        self.pay_button.configure(text="Zapłać", state="disabled")
        for button in self.buttons:
            button.configure(fg_color="#3b8ed0")  # Przywróć domyślny kolor         


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
        cena = bilet["ceny"].get(self.rodzaj_biletu, 0)
        self.pay_button.configure(text=f"Zapłać {cena:.2f} zł", state="normal")

    def start_payment(self):
        """Rozpocznij płatność."""
        if self.selected_bilet is not None:
            total_price = self.selected_bilet["ceny"].get(self.rodzaj_biletu, 0)
            self.app.show_frame("AnimacjaPlacenia", total_price)

    def go_back(self):
        """Akcja przycisku 'Wróć'."""
        previous_screen = getattr(self.app, "previous_page", None)
        if previous_screen == "OkresowyUlgowy_1":
            self.app.show_frame("OkresowyUlgowy_1")
        else:
            self.app.show_frame("MainScreen")
