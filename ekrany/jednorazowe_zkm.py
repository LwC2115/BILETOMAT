import customtkinter as ctk

class JednorazoweZKM(ctk.CTkFrame):
    def __init__(self, app, selected_language):
        super().__init__(app)
        self.app = app
        self.should_reset = True  # Flaga kontrolująca reset ekranu

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Jednorazowe bilety ZKM", font=("Arial", 48, "bold"))
        self.label.pack(pady=20)

        # Kontener dla tabeli
        table_container = ctk.CTkFrame(self, fg_color="transparent")
        table_container.pack(padx=50, pady=20, fill="both", expand=True)

        # Tabela wewnątrz kontenera
        self.table_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True)

        # Nagłówki tabeli
        self.create_table_header()

        # Wiersze tabeli
        self.bilety = [
            {"nazwa": "1-przejazdowy (4.80/2.40 zł)", "normalne": 0, "ulgowe": 0, "cena": 4.80},
            {"nazwa": "75-minutowy (6.00/3.00 zł)", "normalne": 0, "ulgowe": 0, "cena": 6.00},
            {"nazwa": "24-godzinny (22.00/11.00 zł)", "normalne": 0, "ulgowe": 0, "cena": 22.00},
        ]
        self.create_table_rows()

        # Ramka dla sekcji "Do zapłaty" i "Zapłać"
        payment_frame = ctk.CTkFrame(self, fg_color="transparent")
        payment_frame.pack(pady=30)

        # Całkowita kwota do zapłaty
        self.total_label = ctk.CTkLabel(payment_frame, text="Do zapłaty: 0.00 zł", font=("Arial", 36, "bold"))
        self.total_label.pack(side="left", padx=20)

        # Przycisk "Zapłać"
        self.pay_button = ctk.CTkButton(
            payment_frame, text="Zapłać", width=400, height=100, font=("Arial", 36, "bold"),
            command=lambda: self.start_payment(),
            state="disabled"  # Domyślnie wyłączony
        )
        self.pay_button.pack(side="left", padx=20)

        # Przycisk "Wróć"
        self.back_btn = ctk.CTkButton(
            self, text="Wróć", width=200, height=70, font=("Arial", 24, "bold"),
            command=self.go_back
        )
        self.back_btn.place(relx=0.05, rely=0.05, anchor="nw")

    def create_table_header(self):
        """Tworzy nagłówki tabeli."""
        ctk.CTkLabel(self.table_frame, text="Bilet", font=("Arial", 32, "bold"), width=400).grid(row=0, column=0, padx=20, pady=20)
        ctk.CTkLabel(self.table_frame, text="Normalne", font=("Arial", 32, "bold"), width=300).grid(row=0, column=1, padx=20, pady=20)
        ctk.CTkLabel(self.table_frame, text="Ulgowe", font=("Arial", 32, "bold"), width=300).grid(row=0, column=2, padx=20, pady=20)

    def create_table_rows(self):
        """Tworzy wiersze tabeli."""
        for i, bilet in enumerate(self.bilety):
            # Ramka wiersza
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white", corner_radius=20, width=1000, height=100)
            row_frame.grid(row=i + 1, column=0, columnspan=3, padx=10, pady=10)
            row_frame.grid_propagate(False)

            # Treść wiersza
            row_content = ctk.CTkFrame(row_frame, fg_color="transparent")
            row_content.pack(fill="both", expand=True)

            # Kolumna nazwy biletu
            ctk.CTkLabel(row_content, text=bilet["nazwa"], font=("Arial", 28), width=380).pack(side="left", padx=20)

            # Kolumna "Normalny"
            self.create_quantity_controls(row_content, i, "normalne", "left")

            # Kolumna "Ulgowy"
            self.create_quantity_controls(row_content, i, "ulgowe", "left")

    def create_quantity_controls(self, parent, row, column_name, side):
        """Tworzy przyciski do zarządzania ilością biletów."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(side=side, padx=20)

        # Przycisk +
        ctk.CTkButton(
            frame, text="+", width=70, height=70, font=("Arial", 28),
            command=lambda: self.update_quantity(row, column_name, 1)
        ).pack(side="left", padx=10)

        # Ilość
        quantity_label = ctk.CTkLabel(frame, text="0", font=("Arial", 28), width=70)
        quantity_label.pack(side="left", padx=10)

        # Przycisk -
        ctk.CTkButton(
            frame, text="-", width=70, height=70, font=("Arial", 28),
            command=lambda: self.update_quantity(row, column_name, -1)
        ).pack(side="left", padx=10)

        # Przechowujemy referencję do etykiety ilości
        self.bilety[row][f"{column_name}_label"] = quantity_label

    def update_quantity(self, row, column_name, change):
        """Aktualizuje ilość biletów."""
        if column_name not in ["normalne", "ulgowe"]:
            return

        # Zaktualizuj ilość biletów
        self.bilety[row][column_name] += change
        if self.bilety[row][column_name] < 0:
            self.bilety[row][column_name] = 0

        # Zaktualizuj etykietę
        label = self.bilety[row][f"{column_name}_label"]
        label.configure(text=str(self.bilety[row][column_name]))

        # Aktualizuj całkowitą kwotę
        self.update_total_price()

    def update_total_price(self):
        """Aktualizuje całkowitą kwotę do zapłaty i stan przycisku 'Zapłać'."""
        total_price = self.calculate_total_price()
        self.total_label.configure(text=f"Do zapłaty: {total_price:.2f} zł")

        # Blokuj przycisk "Zapłać", jeśli kwota wynosi 0
        if total_price <= 0:
            self.pay_button.configure(state="disabled")
        else:
            self.pay_button.configure(state="normal")

    def go_back(self):
        """Wróć do poprzedniego ekranu."""
        self.should_reset = True  # Ustaw flagę resetu
        self.app.show_frame("MainScreen")

    
    def reset(self):
        """Resetuje ekran do początkowego stanu."""
        for bilet in self.bilety:
            bilet["normalne"] = 0
            bilet["ulgowe"] = 0
            bilet["normalne_label"].configure(text="0")
            bilet["ulgowe_label"].configure(text="0")
        self.update_total_price()
        self.pay_button.configure(state="disabled")  # Zablokuj przycisk "Zapłać"

    def on_enter(self, previous_page):
        """Wykonywane przy wchodzeniu na ekran."""
        if previous_page == "AnimacjaPlacenia":  # Jeśli wracamy z płatności
            self.should_reset = True
        if self.should_reset:
            self.reset()
            self.should_reset = False

    def start_payment(self):
        """Rozpocznij płatność."""
        total_price = self.calculate_total_price()

        # Sprawdź, czy kwota do zapłaty jest większa niż 0
        if total_price > 0:
            # Przekaż kwotę do ekranu płatności
            self.app.show_frame("AnimacjaPlacenia", total_price)
        else:
            # Jeśli kwota wynosi 0, wyłącz przycisk (to może być dodatkowa ochrona)
            self.pay_button.configure(state="disabled")
    def calculate_total_price(self):
        """Oblicza całkowitą kwotę do zapłaty."""
        total_price = 0
        for bilet in self.bilety:
            total_price += bilet["normalne"] * bilet["cena"] + bilet["ulgowe"] * (bilet["cena"] / 2)
        return total_price

         
