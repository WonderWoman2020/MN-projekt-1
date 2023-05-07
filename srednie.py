class Srednie:
    def srednia_ema(self, dane):
        licznik = 0
        n = len(dane)
        a = 2 / (n + 1)
        for d in range(n):
            # pierwszy element listy jest najbardziej oddaloną próbką od dnia dzisiejszego
            licznik = licznik + dane[d] * (1 - a) ** (n - d - 1)

        mianownik = (1 - (1 - a) ** n) / (1 - (1 - a))
        srednia = licznik / mianownik
        return srednia

