class UstawieniaUzytkownika:
    def __init__(self, nazwa_folderu_z_danymi=".\dane",
                 nazwa_pliku_z_danymi="WIG20.csv",
                 ktore_dane="Open",
                 nazwa_folderu_na_wyniki=".\wyniki"):

        self.nazwa_folderu_z_danymi = nazwa_folderu_z_danymi
        self.nazwa_pliku_z_danymi = nazwa_pliku_z_danymi
        self.ktore_dane = ktore_dane  # dla których wartości będzie liczony wskaźnik
        self.nazwa_folderu_na_wyniki = nazwa_folderu_na_wyniki

    def wczytaj_ustawienia_uzytkownika(self):
        czy_pobierac = input("Domyślne ustawienia: "
                             + "\n- Ścieżka do folderu, w którym znajdują się dane: " + self.nazwa_folderu_z_danymi
                             + "\n- Nazwa pliku z danymi: " + self.nazwa_pliku_z_danymi
                             + "\n- Którą grupę danych przeanalizować: " + self.ktore_dane
                             + "\n- Ścieżka do folderu, w którym zapiszą się wyniki: " + self.nazwa_folderu_na_wyniki
                             + "\nCzy chcesz zmienić zahardkodowane domyślne dane? (T/n): ")
        if czy_pobierac == "T":
            self.nazwa_folderu_z_danymi = input("Podaj ścieżkę do folderu, w którym znajdują się dane: ")
            self.nazwa_pliku_z_danymi = input("Podaj nazwę pliku z danymi: ")
            opcja = input("Wybierz którą grupę danych chcesz przeanalizować: \n"
                      "1 - Open / Cena otwarcia\n"
                      "2 - Close / Cena zamknięcia\n"
                      "3 - High / Najwyższa cena\n"
                      "4 - Low / Najniższa cena\n"
                      "Twój wybór (wpisz liczbę 1-4): ")
            self.nazwa_folderu_na_wyniki = input("Podaj ścieżkę do folderu, w którym zapiszą się wyniki: ")
            opcje = {
                "1": "Open",
                "2": "Close",
                "3": "High",
                "4": "Low"
            }
            if opcja not in opcje.keys():
                opcja = "1"
            self.ktore_dane = opcje[opcja]
