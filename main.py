import customtkinter as ctk
from ekrany.main_screen import MainScreen
from ekrany.jednorazowe_zkm import JednorazoweZKM
from ekrany.okresowe_zkm import OkresoweZKM
from ekrany.okresowe_zkm_1 import OkresoweZKM_1
from ekrany.okresowe_mzkzg import OkresoweMZKZG
from ekrany.jednorazowe_mzkzg import JednorazoweMZKZG
from ekrany.podsumowanie import Podsumowanie
from ekrany.animacja_placenia import AnimacjaPlacenia

ctk.set_appearance_mode("light")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bilety")
        
          # Ustawienie domyślnej wielkości na 12 cali
        width = 1152  # 1152 piksele dla 12 cali (przy DPI = 96)
        height = int(width * 9 / 16)  # Proporcje ekranu 16:9
        self.geometry(f"{width}x{height}")  # Ustawienie rozmiaru okna

        self.resizable(False, False)


        self.basket = {}  # Koszyk na bilety: {"nazwa_biletu": {"ilość": x, "cena": y}}

        self.frames = {}
        self.current_frame = None
        self.previous_page = None  # Zapamiętujemy ostatnią stronę
        self.selected_language = "PL"  # Domyślny język

        # Dodaj wszystkie ekrany
        self.add_frame("MainScreen", MainScreen)
        self.add_frame("JednorazoweZKM", JednorazoweZKM)
        self.add_frame("OkresoweZKM", OkresoweZKM)
        self.add_frame("OkresoweZKM_1", OkresoweZKM_1)
        self.add_frame("OkresoweMZKZG", OkresoweMZKZG)
        self.add_frame("JednorazoweMZKZG", JednorazoweMZKZG)
        self.add_frame("Podsumowanie", Podsumowanie)

        self.add_frame("AnimacjaPlacenia", AnimacjaPlacenia)


        # Rozpocznij od głównego ekranu
        self.show_frame("MainScreen")

    def add_frame(self, name, frame_class):
        if name == "AnimacjaPlacenia":  # Dla klasy AnimacjaPlacenia
            frame = frame_class(self)  # Tylko `self` (bez `selected_language`)
        else:  # Dla pozostałych klas ekranów
            frame = frame_class(self, self.selected_language)
        self.frames[name] = frame

    def show_frame(self, name, *args):
        if self.current_frame:
            self.previous_page = self.current_frame.__class__.__name__  # Zapisz nazwę aktualnego ekranu
            self.current_frame.pack_forget()
        frame = self.frames[name]
        if hasattr(frame, "update_content"):
            frame.update_content(*args)  # Przekaż argumenty, jeśli metoda istnieje
        frame.pack(fill="both", expand=True)
        self.current_frame = frame
        
        # Wywołanie on_enter, jeśli ekran je obsługuje
        if hasattr(frame, "on_enter"):
            frame.on_enter(self.previous_page, *args)



    def set_language(self, language):
        self.selected_language = language
        # Po zmianie języka odśwież wszystkie ekrany
        for frame in self.frames.values():
            if hasattr(frame, 'update_language_buttons'):
                frame.update_language_buttons(self.selected_language)
        self.show_frame("MainScreen")  # Odśwież ekran główny po zmianie języka



if __name__ == "__main__":
    app = App()
    app.mainloop()
