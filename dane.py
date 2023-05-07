import algorytm


class KalkulatorDanychDoWykresu:
    def __init__(self, wsk_macd, kalk_przeciec):
        self.wskaznik_macd = wsk_macd
        self.przeciecia = kalk_przeciec

    def wyznacz_narzedzia_do_analizy_danych(self, wartosci):

        # Porzucam próbki początkowe, które były potrzebne do wyliczenia pierwszych wartości wskaźnika
        # macd, czyli te dla których nie da się go wygenerować - ich wyświetlanie byłoby zbędne
        pocz_przedzialu = 0
        konc_przedzialu = 0 + len(wartosci) - (self.wskaznik_macd.okres_wolnej_sredniej + self.wskaznik_macd.okres_signal)
        argumenty_do_wykresu = [*range(pocz_przedzialu, konc_przedzialu, 1)]
        wartosci_do_wykresu = wartosci[self.wskaznik_macd.okres_wolnej_sredniej + self.wskaznik_macd.okres_signal:]

        # wyznaczenie wskaźnika macd oraz jego pochodnych narzędzi
        macd, signal = self.wskaznik_macd.wskaznik_macd(wartosci)
        histogram = self.wskaznik_macd.histogram_punkty(macd, signal)
        przeciecia_pkt_x, przeciecia_pkt_y = self.przeciecia.przeciecia_punkty(macd, signal)
        dni_tuz_po_przecieciach = self.przeciecia.zaokraglone_w_gore_arg_przec(przeciecia_pkt_x)
        if konc_przedzialu in dni_tuz_po_przecieciach:  # warunek brzegowy
            dni_tuz_po_przecieciach.remove(konc_przedzialu)
            dni_tuz_po_przecieciach.append(konc_przedzialu - 1)
        kup_sprzedaj_macd = self.wskaznik_macd.decyzje_kup_sprzedaj(macd, signal, dni_tuz_po_przecieciach)

        # symulacja obrotów akcjami
        transakcje = algorytm.symuluj_obroty_akcjami(algorytm.StanPortfela(1000, 0, wartosci_do_wykresu[0]),
                                                     wartosci_do_wykresu, argumenty_do_wykresu,
                                                     dni_tuz_po_przecieciach, kup_sprzedaj_macd)
        portfel_na_koncu = transakcje.stany_portfeli[-1]
        zyski, dni_transakcji = transakcje.przeanalizuj_zyski_i_straty_miedzy_transakcjami()
        zysk_koncowy = zyski[len(zyski)-1]
        # porzucenie sztucznego zysku początkowego oraz zysku na końcu w stosunku do stanu początkowego
        zyski = zyski[1:len(zyski)-1]
        dni_transakcji = dni_transakcji[1:len(dni_transakcji)-1]

        # wyznaczanie wartości dla osi wykresu
        skala_osi_wartosci = SkalaWartosciOsi()
        skala_osi_wartosci.wyznacz_wartosci_graniczne_danych(wartosci_do_wykresu)
        skala_osi_macd = SkalaWartosciOsi()
        skala_osi_macd.wyznacz_wartosci_graniczne_danych(macd)
        # wykres macd ma mieć linię zero na środku przedziału y
        skala_osi_macd.wysrodkuj_wartosci_graniczne()

        return DaneDoWykresu(wartosci_do_wykresu, argumenty_do_wykresu, macd, signal, histogram,
                             przeciecia_pkt_x, przeciecia_pkt_y, dni_tuz_po_przecieciach, kup_sprzedaj_macd,
                             dni_transakcji, zyski, zysk_koncowy, portfel_na_koncu, skala_osi_wartosci, skala_osi_macd)


class DaneDoWykresu:
    def __init__(self, wartosci_do_wykresu, przedzial_do_wykresu, macd, signal, histogram,
                 przeciecia_pkt_x, przeciecia_pkt_y, dni_tuz_po_przecieciach, kup_sprzedaj_macd, dni_transakcji, zyski,
                 zysk_koncowy, portfel_na_koncu, wartosci_graniczne_wart, wartosci_graniczne_macd):

        self.wartosci = wartosci_do_wykresu
        self.argumenty = przedzial_do_wykresu
        self.macd = macd
        self.signal = signal
        self.histogram = histogram
        # dokładne rzeczywiste liczby wskazujące punkt przecięcia macd i signal
        self.przeciecia_pkt_x = przeciecia_pkt_x
        self.przeciecia_pkt_y = przeciecia_pkt_y
        # dni to zaokrąglone w górę do najbliższej kolejnej wartości całkowitej punkty
        # przecięcia - punkty dla których w przedziale między nimi, a poprzednim punktem,
        # nastąpiło przecięcie linii macd i signal - dopiero w punktach tuż po przecięciu
        # tych linii mam informację ze wskaźnika, że powinnam kupić lub sprzedać
        self.dni_tuz_po_przecieciach = dni_tuz_po_przecieciach
        self.kup_sprzedaj_macd = kup_sprzedaj_macd

        # wyniki działania algorytmu zakupu / sprzedaży akcji na podstawie wskaźnika macd
        self.dni_transakcji = dni_transakcji
        self.zyski = zyski
        self.zysk_koncowy = zysk_koncowy
        self.portfel_na_koncu = portfel_na_koncu

        self.skala_wartosci_y1 = wartosci_graniczne_wart
        self.skala_wartosci_y2 = wartosci_graniczne_macd

    def __len__(self):
        return len(self.wartosci)

    def zwroc_przedzial_danych(self, poczatek, koniec):
        w = self.wartosci[poczatek:koniec]
        przedz = self.argumenty[poczatek:koniec]
        m = self.macd[poczatek:koniec]
        s = self.signal[poczatek:koniec]
        h = self.histogram[poczatek:koniec]
        p_x = []
        p_y = []
        # z listy punktów przecięcia wybieram tylko te, które
        # mieszczą się w wyznaczanym przedziale danych
        for x, y in zip(self.przeciecia_pkt_x, self.przeciecia_pkt_y):
            if poczatek <= x < koniec:
                p_x.append(x)
                p_y.append(y)
            if x >= koniec:
                break
        dni = []
        liczba_poprzednich_przeciec = 0
        for d in self.dni_tuz_po_przecieciach:
            if poczatek <= d < koniec:
                dni.append(d)
            if d < poczatek:
                liczba_poprzednich_przeciec = liczba_poprzednich_przeciec+1
            if d >= koniec:
                break

        # decyzji kup/sprzedaj jest tyle samo ile wszystkich punktów przecięcia, muszę więc
        # pominąć tyle decyzji, ile punktów przecięcia napotkałam w części danych
        # przed przedziałem, który chcę wyciąć, oraz wziąć tylko tyle decyzji, ile
        # punktów przecięcia mieści się w wycinanym przedziale
        k_s = self.kup_sprzedaj_macd[liczba_poprzednich_przeciec:liczba_poprzednich_przeciec+len(dni)]

        dni_transakcji = []
        liczba_poprzednich_transakcji = 0
        for d_t in self.dni_transakcji:
            if poczatek <= d_t < koniec:
                dni_transakcji.append(d_t)
            if poczatek > d_t >= 0:
                liczba_poprzednich_transakcji = liczba_poprzednich_transakcji+1
            if d_t >= koniec:
                break

        z = self.zyski[liczba_poprzednich_transakcji:liczba_poprzednich_transakcji+len(dni_transakcji)]

        return DaneDoWykresu(w, przedz, m, s, h, p_x, p_y, dni, k_s, dni_transakcji, z, self.zysk_koncowy,
                             self.portfel_na_koncu, self.skala_wartosci_y1, self.skala_wartosci_y2)


class SkalaWartosciOsi:
    def __init__(self, granica_max=0, granica_min=0, odstep_na_osi=0):
        self.granica_max = granica_max
        self.granica_min = granica_min
        self.odstep = odstep_na_osi

    def wyznacz_wartosci_graniczne_danych(self, wartosci):
        max_z_wartosci = max(wartosci)
        min_z_wartosci = min(wartosci)
        odstep = int(abs(max_z_wartosci - min_z_wartosci) / 10) + 1
        rzad_wielkosci = self.wyznacz_rzad_wielkosci(odstep)

        # zaokrąglenie w górę do najbliższej pełnej wartości o 1 rząd wielkości mniejszej
        odstep = int(odstep / (10 ** (rzad_wielkosci - 1))) * (10 ** (rzad_wielkosci - 1)) + (
                    10 ** (rzad_wielkosci - 1))
        # zaokrąglenie do najbliższego pełnego odstępu na osi
        if max_z_wartosci >= 0:
            granica_max = int(max_z_wartosci / odstep) * odstep + odstep
        else:
            granica_max = int(max_z_wartosci / odstep) * odstep
        if min_z_wartosci >= 0:
            granica_min = int(min_z_wartosci / odstep) * odstep
        else:
            granica_min = int(min_z_wartosci / odstep) * odstep - odstep

        self.granica_max = granica_max
        self.granica_min = granica_min
        self.odstep = odstep

    def wysrodkuj_wartosci_graniczne(self):
        if abs(self.granica_max) >= abs(self.granica_min):
            self.granica_min = - abs(self.granica_max)
        else:
            self.granica_max = abs(self.granica_min)

    def wyznacz_rzad_wielkosci(self, liczba):
        zmienna = liczba
        rzad_wielkosci = 0
        while zmienna != 0:
            rzad_wielkosci = rzad_wielkosci + 1
            zmienna = int(zmienna / 10)
        return rzad_wielkosci

