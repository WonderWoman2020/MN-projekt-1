class Wskaznik:
    def __init__(self, kalk_srednich, okres_szybkiej_sr=12, okres_wolnej_sr=26, okres_signal=9):
        self.srednie = kalk_srednich
        self.okres_szybkiej_sredniej = okres_szybkiej_sr
        self.okres_wolnej_sredniej = okres_wolnej_sr
        self.okres_signal = okres_signal

    def macd_linia_punkty(self, dane):
        # liczba punktów linii macd do policzenia
        # (pierwsze param2 próbek to próbki początkowe,
        # dla których nie ma jeszcze jak policzyć linii
        # macd)
        n = len(dane) - self.okres_wolnej_sredniej
        macd_punkty = []
        for d in range(n):
            # param1 wcześniejszych próbek przed próbką, dla której
            # będziemy wyliczać wartość macd
            indeks_szybka1 = d + (self.okres_wolnej_sredniej - self.okres_szybkiej_sredniej)
            indeks_szybka2 = d + self.okres_wolnej_sredniej
            # analogicznie param2 wcześniejszych próbek
            indeks_wolna1 = d + 0
            indeks_wolna2 = d + self.okres_wolnej_sredniej

            ema_szybka = self.srednie.srednia_ema(
                dane[indeks_szybka1:indeks_szybka2 + 1])  # +1 żeby wziąć też próbkę z dnia dzisiejszego
            ema_wolna = self.srednie.srednia_ema(dane[indeks_wolna1:indeks_wolna2 + 1])
            wartosc = ema_szybka - ema_wolna

            macd_punkty.append(wartosc)

        return macd_punkty

    def signal_linia_punkty(self, macd_punkty):
        n = len(macd_punkty) - self.okres_signal
        signal_punkty = []
        for m in range(n):
            indeks1 = m + 0
            indeks2 = m + self.okres_signal

            wartosc = self.srednie.srednia_ema(macd_punkty[indeks1:indeks2])
            signal_punkty.append(wartosc)
        return signal_punkty

    def wskaznik_macd(self, dane):
        macd_punkty = self.macd_linia_punkty(dane)
        signal_punkty = self.signal_linia_punkty(macd_punkty)
        # usuwam wartości macd, dla których nie ma jeszcze linii SIGNAL (próbki początkowe)
        macd_punkty = macd_punkty[self.okres_signal:]
        return macd_punkty, signal_punkty

    def kup_sprzedaj(self, macd_linia, signal_linia, dzien_po_przecieciu):
        # sprawdzam która wartość wskaźnika była mniejsza do drugiej
        # w dzień przed przecięciem się obu linii
        if macd_linia[dzien_po_przecieciu - 1] <= signal_linia[dzien_po_przecieciu - 1]:
            # MACD przetnie SIGNAL od dołu
            return "kup"
        else:
            return "sprzedaj"

    def decyzje_kup_sprzedaj(self, macd_linia, signal_linia, punkty_x, przesuniecie=0):
        decyzje = []
        for x in punkty_x:
            decyzje.append(self.kup_sprzedaj(macd_linia, signal_linia, x+przesuniecie))
        return decyzje

    def histogram_punkty(self, macd_punkty, signal_punkty):
        n = len(macd_punkty)
        histogram = []
        for i in range(n):
            histogram.append(macd_punkty[i] - signal_punkty[i])
        return histogram
