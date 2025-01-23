import customtkinter as ctk
from PIL import Image

class MainScreen(ctk.CTkFrame):
    def __init__(self, app, selected_language):
        super().__init__(app)
        self.app = app
        self.selected_language = selected_language

        self.flags = {
            "PL": ctk.CTkImage(Image.open("ekrany/flags/pl.png"), size=(40, 40)),
            "EN": ctk.CTkImage(Image.open("ekrany/flags/en.png"), size=(40, 40)),
            "DE": ctk.CTkImage(Image.open("ekrany/flags/de.png"), size=(40, 40)),
            "FR": ctk.CTkImage(Image.open("ekrany/flags/fr.png"), size=(40, 40)),
        }
 

        # Nagłówek
        self.label = ctk.CTkLabel(self, text="Wybierz rodzaj biletu", font=("Arial", 40, "bold"))  # Powiększona czcionka
        self.label.pack(pady=30)  # Większy odstęp nad i pod nagłówkiem

        # Ramka dla przycisków głównych
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=50)  # Większy odstęp od góry

        # Powiększone przyciski główne
        self.jednorazowe_zkm_btn = ctk.CTkButton(
            button_frame, text="Jednorazowe ZKM", width=400, height=150, font=("Arial", 30, "bold"),
            command=lambda: app.show_frame("JednorazoweZKM")
        )
        self.jednorazowe_zkm_btn.grid(row=0, column=0, padx=30, pady=20)

        self.okresowe_zkm_btn = ctk.CTkButton(
            button_frame, text="Okresowe ZKM", width=400, height=150, font=("Arial", 30, "bold"),
            command=lambda: app.show_frame("AnimacjaWczytaniaKarty")
        )
        self.okresowe_zkm_btn.grid(row=0, column=1, padx=30, pady=20)

        self.jednorazowe_mzkzg_btn = ctk.CTkButton(
            button_frame, text="Jednorazowe MZKZG", width=400, height=150, font=("Arial", 30, "bold"),
            command=lambda: app.show_frame("JednorazoweMZKZG")
        )
        self.jednorazowe_mzkzg_btn.grid(row=1, column=0, padx=30, pady=20)

        self.okresowe_mzkzg_btn = ctk.CTkButton(
            button_frame, text="Okresowe MZKZG", width=400, height=150, font=("Arial", 30, "bold"),
            command=lambda: app.show_frame("AnimacjaWczytaniaKartyMetro")
        )
        self.okresowe_mzkzg_btn.grid(row=1, column=1, padx=30, pady=20)

        # Przyciski językowe przeniesione do lewego dolnego rogu
        flag_frame = ctk.CTkFrame(self, fg_color="transparent")
        flag_frame.place(relx=0.98, rely=0.95, anchor="se")  # Relatywne pozycjonowanie w lewym dolnym rogu

        languages = ["PL", "EN", "DE", "FR"]
        self.language_buttons = []

        for lang in languages:
            bg_color = "#2a6ca3" if lang == selected_language else "#3b8ed0"

            lang_button = ctk.CTkButton(
                flag_frame,
                text="",
                image=self.flags[lang],  # Ustawiamy ikonę flagi
                width=80,
                height=50,
                font=("Arial", 20, "bold"),  # Powiększona czcionka
                fg_color=bg_color,
                command=lambda l=lang: self.app.set_language(l),  # Zmiana języka
            )
            lang_button.pack(side="left", padx=10)  # Odstępy między przyciskami językowymi
            self.language_buttons.append(lang_button)

    def update_language_buttons(self, selected_language):
        # Aktualizacja kolorów przycisków językowych
        for button in self.language_buttons:
            if button.cget("text") == selected_language:
                button.configure(fg_color="#003366")  # Wybrany język
            else:
                button.configure(fg_color="#3b8ed0")  # Inne języki
