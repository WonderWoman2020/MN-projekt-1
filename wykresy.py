import matplotlib.pyplot as plt


class Wykres:
    def __init__(self, kolory, tytuly, co_wyswietlac):
        self.kolory = kolory
        self.tytuly = tytuly
        self.co_wyswietlac = co_wyswietlac
        self.dane = None
        self.nazwa_wykresu_do_zapisu = None

    def dodaj_dane_do_wykresu(self, ax1, ax2):
        # wartości z pliku są zawsze wyświetlane
        ax1.plot(self.dane.argumenty, self.dane.wartosci,
                 color=self.kolory.wartosci, label=self.tytuly.os_y1)
        if self.co_wyswietlac.wsk_macd:
            ax2.plot(self.dane.argumenty, self.dane.macd, color=self.kolory.macd, label='macd')
            ax2.plot(self.dane.argumenty, self.dane.signal, color=self.kolory.signal, label='signal')
        if self.co_wyswietlac.histogram:
            ax2.bar(self.dane.argumenty, self.dane.histogram, color=self.kolory.histogram, label='histogram')
        if self.co_wyswietlac.przeciecia:
            # punkty przecięcia MACD z SIGNAL
            ax2.plot(self.dane.przeciecia_pkt_x, self.dane.przeciecia_pkt_y, self.kolory.przeciecia + "x")
            # punkty przecięcia na wykresie danych, kółka - zyskowne transakcje, krzyżyki - stratne
            for d, i in zip(self.dane.dni_transakcji, range(len(self.dane.dni_transakcji))):
                if self.dane.zyski[i] >= 1:
                    ax1.plot(d, self.dane.wartosci[d - self.dane.argumenty[0]], "g" + "o")
                else:
                    ax1.plot(d, self.dane.wartosci[d - self.dane.argumenty[0]], self.kolory.przeciecia + "x")
            for d, i in zip(self.dane.dni_tuz_po_przecieciach, range(len(self.dane.dni_tuz_po_przecieciach))):
                # decyzje kup / sprzedaj wskaźnika macd
                ax1.annotate(self.dane.kup_sprzedaj_macd[i], (d, self.dane.wartosci[d - self.dane.argumenty[0]]))
        if self.co_wyswietlac.linie_przeciec:
            # pomocnicze linie w miejscach przecięć na wykresie wskaźnika i wartości
            for p_x in self.dane.przeciecia_pkt_x:
                ax1.axvline(x=p_x, color=self.kolory.linie_przeciec, linestyle='--')
                ax2.axvline(x=p_x, color=self.kolory.linie_przeciec, linestyle='--')

        return ax1, ax2

    def ustaw_wyglad_wykresu(self, ax1, ax2):
        # skalowanie osi
        ax1.set_ylim(self.dane.skala_wartosci_y1.granica_min, self.dane.skala_wartosci_y1.granica_max)
        ax2.set_ylim(self.dane.skala_wartosci_y2.granica_min, self.dane.skala_wartosci_y2.granica_max)
        # wspólna oś x dla obu wykresów, podziałka co 1/20 długości danych
        ax2.set_xticks([*range(self.dane.argumenty[0],
                               self.dane.argumenty[len(self.dane.argumenty) - 1] + 2,
                               int(len(self.dane.wartosci) / 20))])

        # linia 0 na wykresie wskaźnika
        ax2.axhline(y=0, color=self.kolory.linia_zero, linestyle='--')
        # brak przerwy między wykresami
        plt.subplots_adjust(hspace=0)
        # włączenie pokazywania legend na wykresach
        ax1.legend(loc="upper right")
        ax2.legend(loc="upper right")

        return ax1, ax2

    def ustaw_tytuly_wykresu(self, ax1, ax2):
        plt.suptitle(self.tytuly.wykres, fontsize=16, y=0.92)  # y - odstęp tytułu od wykresu
        plt.xlabel(self.tytuly.os_x, fontsize=12, loc='right')
        ax1.set_ylabel(self.tytuly.os_y1, fontsize=12, labelpad=10, loc='top')
        ax2.set_ylabel(self.tytuly.os_y2,  fontsize=12, labelpad=10, loc='top')
        return ax1, ax2

    def rysuj_wykres(self, nazwa, dane):
        self.dane = dane
        self.nazwa_wykresu_do_zapisu = nazwa

        # stworzenie głównego wykresu
        fig = plt.figure(figsize=(18, 12))
        # stworzenie 2 składowych wykresów, osobno na wartości i wskaźnik macd
        ax1 = plt.subplot2grid(shape=(5, 1), loc=(0, 0), rowspan=3)
        ax2 = plt.subplot2grid(shape=(5, 1), loc=(3, 0), rowspan=2, sharex=ax1)

        ax1, ax2 = self.dodaj_dane_do_wykresu(ax1, ax2)
        ax1, ax2 = self.ustaw_wyglad_wykresu(ax1, ax2)
        ax1, ax2 = self.ustaw_tytuly_wykresu(ax1, ax2)

        # zapisanie wykresu
        plt.savefig(self.nazwa_wykresu_do_zapisu, bbox_inches='tight')  # bbox_inches - brak białego pola wokół wykresu
        plt.close()
        # plt.show()

        print("Zapisano wykres " + self.nazwa_wykresu_do_zapisu)

    def rysuj_wykres_podzielony_na_czesci(self, nazwa, dane, liczba_wykresow):
        dlug = int(len(dane) / liczba_wykresow)
        for i in range(liczba_wykresow):
            nazwa_pliku1 = nazwa[:-4]  # ucięcie rozszerzenia .png
            nazwa_pliku1 = nazwa_pliku1 + "_" + str(i + 1) + ".png"
            poczatek = 0 + i * dlug
            koniec = (i + 1) * dlug
            dane_czesc = dane.zwroc_przedzial_danych(poczatek, koniec)
            self.rysuj_wykres(nazwa_pliku1, dane_czesc)


class KoloryWykresu:
    def __init__(self, linia_wartosci='forestgreen',
                 linia_macd='royalblue',
                 linia_signal='darkorange',
                 histogram='darkred',
                 przeciecia='r',
                 linie_przeciec='#999999',
                 linia_zero='limegreen'):

        self.wartosci = linia_wartosci
        self.macd = linia_macd
        self.signal = linia_signal
        self.histogram = histogram
        self.przeciecia = przeciecia
        self.linie_przeciec = linie_przeciec
        self.linia_zero = linia_zero


class TytulyWykresu:
    def __init__(self, nazwa_wartosci, tytul_wykresu=None,
                 tytul_osi_x="Dni", tytul_osi_y1=None, tytul_osi_y2="Wskaźnik MACD"):

        self.wykres = tytul_wykresu
        self.os_y1 = tytul_osi_y1
        self.os_y2 = tytul_osi_y2
        self.os_x = tytul_osi_x

        if tytul_wykresu is None:
            self.wykres = "Wskaźnik MACD - " + nazwa_wartosci
        if tytul_osi_y1 is None:
            self.os_y1 = "Wartości " + nazwa_wartosci


class CoWyswietlacNaWykresie:
    def __init__(self, pokaz_wsk_macd=True, pokaz_hist=False, pokaz_przeciecia=False,
                 pokaz_linie_od_przeciec=False):

        self.wsk_macd = pokaz_wsk_macd
        self.histogram = pokaz_hist
        self.przeciecia = pokaz_przeciecia
        self.linie_przeciec = pokaz_linie_od_przeciec
