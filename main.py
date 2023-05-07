import pandas as pd
import os

import algorytm
import macd
import przeciecia
import srednie
import wykresy
import wczytywanie
import dane


# wczytanie poleceń użytkownika
ustawienia = wczytywanie.UstawieniaUzytkownika()
ustawienia.wczytaj_ustawienia_uzytkownika()

# wczytanie danych
sciezka_dane = ustawienia.nazwa_folderu_z_danymi + "\\"\
               + ustawienia.nazwa_pliku_z_danymi

df = pd.read_csv(sciezka_dane)

# przygotowanie folderów na wyniki
nazwa_pliku_z_danymi_bez_rozszerzenia = os.path.splitext(ustawienia.nazwa_pliku_z_danymi)[0]
sciezka_wyniki = ustawienia.nazwa_folderu_na_wyniki + "\\" \
                 + nazwa_pliku_z_danymi_bez_rozszerzenia \
                 + "_" \
                 + ustawienia.ktore_dane

if not os.path.exists(sciezka_wyniki):
    os.makedirs(sciezka_wyniki)

# ustawianie parametrów wskaźnika macd i obiektów służących do obliczenia danych
srednia_kalk = srednie.Srednie()
wskaznik_kalk = macd.Wskaznik(srednia_kalk)
punkty_przec_kalk = przeciecia.Przeciecia()
dane_kalk = dane.KalkulatorDanychDoWykresu(wskaznik_kalk, punkty_przec_kalk)
# obliczanie macd, signal, histogramu, punktów przecięcia itd., symulacja obrotów akcjami
dane_caly_wykres = dane_kalk.wyznacz_narzedzia_do_analizy_danych(df[ustawienia.ktore_dane].to_list())

# rysowanie wykresu
ust1 = wykresy.KoloryWykresu(linia_wartosci='pink')
ust2 = wykresy.TytulyWykresu(nazwa_pliku_z_danymi_bez_rozszerzenia)
ust3 = wykresy.CoWyswietlacNaWykresie(pokaz_hist=True)
wykresik = wykresy.Wykres(ust1, ust2, ust3)
wykresik.rysuj_wykres(sciezka_wyniki +"\\" +"wykres_caly.png", dane_caly_wykres)

# zapisanie wykresu podzielonego na części, do dalszej analizy
liczba_wykresow = 10
ust1_inne = wykresy.KoloryWykresu()
ust3_inne = wykresy.CoWyswietlacNaWykresie(pokaz_przeciecia=True, pokaz_linie_od_przeciec=True, pokaz_hist=True)
wykresik_inny = wykresy.Wykres(ust1_inne, ust2, ust3_inne)
wykresik_inny.rysuj_wykres_podzielony_na_czesci(sciezka_wyniki +"\\" +"wykres_czesciowy.png",
                                                dane_caly_wykres, liczba_wykresow)


print("\nWykresy zostały zapisane w folderze "+sciezka_wyniki+"!")

# wynik działania algorytmu obrotu akcjami
print("\nPortfel na początku: \n" + str(algorytm.StanPortfela(1000, 0, dane_caly_wykres.wartosci[0])))
print("\nPortfel na końcu: \n" + str(dane_caly_wykres.portfel_na_koncu))
print("\nCałkowity zysk po badanym okresie: "+str(dane_caly_wykres.zysk_koncowy))

input("\nNaciśnij enter, aby zakończyć program")
