import math


class Punkt:
    def __init__(self, x_wart, y_wart, nazwa="p"):
        self.x = x_wart
        self.y = y_wart
        self.nazwa = nazwa

    def __str__(self):
        return "Punkt " + self.nazwa + "(" + str(self.x) + ", " + str(self.y) + ")"


class Przeciecia:
    # pomiędzy poszczególnymi punktami są linie proste na wykresie
    # więc punkty przecięcia wykresów można znaleźć sprawdzając każdą taką
    # krótką linię pomiędzy dwoma punktami dla obu funkcji i szukając,
    # czy się przetną pomiędzy tymi dwoma argumentami
    def przeciecia_punkty(self, krzywa1, krzywa2, przesuniecie=0):
        n = len(krzywa1)
        punkty = []
        x_ret = []
        y_ret = []
        for i in range(n - 1):
            p1k1 = Punkt(i + przesuniecie, krzywa1[i])
            p2k1 = Punkt(i + 1 + przesuniecie, krzywa1[i + 1])
            p1k2 = Punkt(i + przesuniecie, krzywa2[i])
            p2k2 = Punkt(i + 1 + przesuniecie, krzywa2[i + 1])
            a1, b1 = self.wyznacz_funkcje_liniowa(p1k1, p2k1)
            a2, b2 = self.wyznacz_funkcje_liniowa(p1k2, p2k2)
            if (a1 - a2) != 0:
                x = (b2 - b1) / (a1 - a2)  # argument, dla którego wystąpiło przecięcie
                if i + przesuniecie <= x < i + 1 + przesuniecie:
                    y = a1 * x + b1
                    punkty.append(Punkt(x, y))
                    x_ret.append(x)
                    y_ret.append(y)

        return x_ret, y_ret

    def wyznacz_funkcje_liniowa(self, p1, p2):
        # współczynnik kierunkowy a
        a = (p1.y - p2.y) / (p1.x - p2.x)
        # przesunięcie
        b = p1.y - a * p1.x
        return a, b

    def zaokraglone_w_gore_arg_przec(self, punkty_x):
        x_zaokr = []
        for x in punkty_x:
            x_zaokr.append(math.ceil(x))  # najbliższy następny dzień po przecięciu MACD i SIGNAL
        return x_zaokr
