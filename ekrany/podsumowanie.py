import customtkinter as ctk
from PIL import Image


class Podsumowanie(ctk.CTkFrame):
    def __init__(self, app, selected_language):
        super().__init__(app)
        self.app = app

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Podsumowanie", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        # Przycisk Wróć
        self.back_btn = ctk.CTkButton(
            self, text="Wróć", width=120, height=50, font=("Arial", 18, "bold"),
            command=self.go_back
        )
        self.back_btn.place(relx=0.05, rely=0.05, anchor="nw")

        # Element listy biletu
        self.ticket_frame = ctk.CTkFrame(self, width=1000, height=100, fg_color="white", corner_radius=200)
        self.ticket_frame.place(relx=0.5, rely=0.3, anchor="center")

        # Załaduj ikonę kosza
        trash_icon_image = ctk.CTkImage(
            light_image=Image.open("./ekrany/trash.png"),
            size=(40, 40)
        )

        # Ikona kosza
        self.delete_btn = ctk.CTkButton(
            self.ticket_frame, text="", width=100, height=100, fg_color="#D32F2F", image=trash_icon_image,
            hover_color="#B71C1C", command=self.delete_ticket
        )
        self.delete_btn.place(relx=0.05, rely=0.5, anchor="center")

        # Nazwa biletu
        self.ticket_label = ctk.CTkLabel(self.ticket_frame, text="1-przejazdowy ZKM Gdynia", font=("Arial", 18))
        self.ticket_label.place(relx=0.4, rely=0.5, anchor="center")

        # Przycisk zmniejszenia ilości
        self.minus_btn = ctk.CTkButton(
            self.ticket_frame, text="-", width=100, height=100, font=("Arial", 24, "bold"),
            fg_color="#3b8ed0", hover_color="#2a6ca3", command=self.decrease_quantity
        )
        self.minus_btn.place(relx=0.75, rely=0.5, anchor="center")

        # Ilość biletów
        self.quantity_label = ctk.CTkLabel(
            self.ticket_frame,
            text=str(self.get_ticket_quantity()),  # Dynamiczne ustawienie ilości biletów
            font=("Arial", 24, "bold")
        )
        self.quantity_label.place(relx=0.85, rely=0.5, anchor="center")

        # Przycisk zwiększenia ilości
        self.plus_btn = ctk.CTkButton(
            self.ticket_frame, text="+", width=100, height=100, font=("Arial", 24, "bold"),
            fg_color="#3b8ed0", hover_color="#2a6ca3", command=self.increase_quantity
        )
        self.plus_btn.place(relx=0.95, rely=0.5, anchor="center")

        # Tekst "Wrzuć gotówkę lub zbliż kartę"
        self.payment_instruction = ctk.CTkLabel(
            self, text="Wrzuć gotówkę lub zbliż kartę do czytnika", font=("Arial", 24, "bold")
        )
        self.payment_instruction.place(relx=0.5, rely=0.5, anchor="center")

        # Przyciski na dole ekranu
        self.cancel_btn = ctk.CTkButton(
            self, text="Zrezygnuj z zakupu\n(zwróć gotówkę)", width=250, height=100, font=("Arial", 18, "bold"),
            fg_color="#D32F2F", hover_color="#B71C1C", command=self.cancel_purchase
        )
        self.cancel_btn.place(relx=0.15, rely=0.85, anchor="center")

        self.add_ticket_btn = ctk.CTkButton(
            self, text="Dodaj kolejny bilet", width=250, height=100, font=("Arial", 18, "bold"),
            fg_color="#3b8ed0", hover_color="#2a6ca3", command=lambda: self.app.show_frame("MainScreen")
        )
        self.add_ticket_btn.place(relx=0.4, rely=0.85, anchor="center")

        # Czarna linia
        self.line_canvas = ctk.CTkCanvas(self, width=820, height=4, bg="black", highlightthickness=0)
        self.line_canvas.place(relx=0.55, rely=0.8, anchor="w")
        self.line_canvas.create_line(0, 0, 500, 0, fill="black", width=2)

        # Kwota do zapłaty
        self.payment_label = ctk.CTkLabel(self, text="Do zapłaty zostało:", font=("Arial", 32, "bold"))
        self.payment_label.place(relx=0.54, rely=0.75, anchor="w")

        self.total_amount = ctk.CTkLabel(self, text="0zł", font=("Arial", 42, "bold")) # tutaj zmienić 0zł
        self.total_amount.place(relx=0.95, rely=0.85, anchor="e")

        # Zaktualizuj koszyk
        self.update_basket()

    def go_back(self):
        """Przejdź do poprzedniego ekranu."""
        previous_page = self.app.previous_page  # Pobierz poprzednią stronę
        if previous_page:
            self.app.show_frame(previous_page)  # Przejdź do poprzedniej strony
        else:
            self.app.show_frame("MainScreen")  # Domyślnie wróć na ekran główny

    def get_ticket_quantity(self):
        """Pobierz ilość biletów z koszyka, domyślnie 1."""
        if self.app.basket:
            for ticket, details in self.app.basket.items():
                return details.get("ilość", 1)
        return 1

    def update_basket(self):
        """Aktualizuj ilość biletów i cenę."""
        total_price = 0
        for ticket, details in self.app.basket.items():
            ilość = details["ilość"]
            cena = details["cena"]
            total_price += ilość * cena

            # Zaktualizuj etykietę ilości
            self.quantity_label.configure(text=str(ilość))

        self.total_amount.configure(text=f"{total_price:.2f} zł")

    def delete_ticket(self):
        for ticket in list(self.app.basket.keys()):
            del self.app.basket[ticket]
            break
        self.update_basket()

    def decrease_quantity(self):
        for ticket, details in self.app.basket.items():
            if details["ilość"] > 0:
                details["ilość"] -= 1
            break
        self.update_basket()

    def increase_quantity(self):
        for ticket, details in self.app.basket.items():
            details["ilość"] += 1
            break
        self.update_basket()

    def cancel_purchase(self):
        print("Rezygnacja z zakupu")
