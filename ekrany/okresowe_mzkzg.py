import customtkinter as ctk

class OkresoweMZKZG(ctk.CTkFrame):
    def __init__(self, app, selected_language):
        super().__init__(app)
        self.app = app

        self.label = ctk.CTkLabel(self, text="Okresowe MZKZG", font=("Arial", 24))
        self.label.pack(pady=20)

        self.back_btn = ctk.CTkButton(
            self, text="Wróć", width=200, height=50,
            command=lambda: app.show_frame("MainScreen")
        )
        self.back_btn.pack(pady=10)

        self.next_btn = ctk.CTkButton(
            self, text="Następny", width=200, height=50,
            command=lambda: app.show_frame("Podsumowanie")
        )
        self.next_btn.pack(pady=10)
