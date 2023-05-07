class StanPortfela:
    def __init__(self, liczba_akcji, pieniadze_w_kieszeni, cena_akcji):
        self.liczba_akcji = liczba_akcji
        self.pieniadze_w_kieszeni = pieniadze_w_kieszeni
        self.cena_akcji = cena_akcji

    def __str__(self):
        napis = "Stan portfela: \n" + "Liczba akcji: " + str(self.liczba_akcji) \
                + "\nPieniadze w kieszeni: " + str(self.pieniadze_w_kieszeni)\
                + "\nAktualna cena akcji: " + str(self.cena_akcji)
        return napis

    def oblicz_wartosc_portfela(self):
        return (self.liczba_akcji * self.cena_akcji) + self.pieniadze_w_kieszeni


class HistoriaTransakcji:
    def __init__(self):
        # pierwszym stanem jest stan na wejściu portfela, a ostatnim stan na koniec badanego okresu
        # stany pomiędzy nimi to stany po dokonanych transakcjach
        self.stany_portfeli = []
        self.dni_transakcji = []
        self.decyzje = []

    def dodaj_transakcje(self, stan_portfela, dzien, decyzja):
        self.stany_portfeli.append(stan_portfela)
        self.dni_transakcji.append(dzien)
        self.decyzje.append(decyzja)

    def oblicz_zysk(self, portfel_na_poczatku, portfel_na_koncu):
        zysk = portfel_na_koncu.oblicz_wartosc_portfela() / portfel_na_poczatku.oblicz_wartosc_portfela()
        return zysk

    def przeanalizuj_zyski_i_straty_miedzy_transakcjami(self):
        zyski = []
        # na początku dostajemy 1000 akcji i nie wiemy co było przedtem, więc stan początkowy przyjmuję jako zysk = 1
        zyski.append(1)
        for i in range(len(self.stany_portfeli)-2):
            pierwszy_portfel = self.stany_portfeli[i]
            drugi_portfel = self.stany_portfeli[i+1]
            # obliczamy zysk dla drugiego portfela, w stosunku do poprzedniego
            zyski.append(self.oblicz_zysk(pierwszy_portfel, drugi_portfel))

        # zysk ostatniego portfela względem początkowego
        zyski.append(self.oblicz_zysk(self.stany_portfeli[0], self.stany_portfeli[-1]))

        return zyski, self.dni_transakcji


# alorytm sprzedaje wszystkie akcje lub kupuje je za wszystkie dostępne środki
# bezpośrednio na podstawie decyzji wynikających ze wskaźnika macd
def symuluj_obroty_akcjami(portfel_na_poczatku, wartosci, argumenty, dni_tuz_po_przecieciach, kup_sprzedaj_macd):

    historia_transakcji = HistoriaTransakcji()
    historia_transakcji.dodaj_transakcje(portfel_na_poczatku, -1, "poczatek")

    liczba_akcji = portfel_na_poczatku.liczba_akcji
    pieniadze = portfel_na_poczatku.pieniadze_w_kieszeni
    for dzien, i in zip(dni_tuz_po_przecieciach, range(len(dni_tuz_po_przecieciach))):
        kurs_w_danym_dniu = wartosci[dzien - argumenty[0]]
        decyzja = kup_sprzedaj_macd[i]
        if decyzja == "sprzedaj":
            if liczba_akcji > 0:
                pieniadze = pieniadze + liczba_akcji * kurs_w_danym_dniu
                liczba_akcji = 0
        else:
            if pieniadze > 0:
                # maksymalna możliwa liczba pełnych akcji do kupienia
                liczba_akcji = liczba_akcji + int(pieniadze / kurs_w_danym_dniu)
                # odjęcie tylko tylu pieniędzy, ile zapłacono za pełne akcje, reszta zostaje
                pieniadze = pieniadze - int(pieniadze / kurs_w_danym_dniu) * kurs_w_danym_dniu

        stan_portfela = StanPortfela(liczba_akcji, pieniadze, kurs_w_danym_dniu)
        historia_transakcji.dodaj_transakcje(stan_portfela, dzien, decyzja)

    portfel_na_koncu = StanPortfela(liczba_akcji, pieniadze, wartosci[-1])
    historia_transakcji.dodaj_transakcje(portfel_na_koncu, argumenty[-1]+1, "koniec")

    return historia_transakcji
