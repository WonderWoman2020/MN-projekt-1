# MN-projekt-1

## Opis

Projekt z Metod Numerycznych - wyznaczanie wartości wskaźnika MACD na podstawie danych wejściowych z giełdy. Program przyjmuje dane o akcjach z giełdy (w formacie `.csv`, przykładowe pliki są w folderze `dane`), oblicza wskaźnik MACD i rysuje na tej podstawie wykresy zestawiające wartości wskaźnika i akcji. Algorytm przeprowadza również symulację obrotu akcjami i podejmuje decyzję o ich kupnie lub sprzedaży na podstawie wartości wskaźnika. Decyzje, jakie algorytm podjął, są również zaznaczane na wykresach.

Program może służyć jako proste narzędzie wspomagające, jeśli posiadamy dane o akcjach z pewnego okresu czasu wstecz i chcemy używać wskaźnika MACD do podjęcia decyzji o obrocie akcjami.

## Przykładowe wykresy generowane przez program

1. Wykres z całego badanego okresu (1000 dni):

![wykres 1](./przykłady/wykres_caly.png)

2. Wykres szczegółowy, pokazujący wycinek czasu z badanego okresu (100 dni):

![wykres 2](./przykłady/wykres_czesciowy_1.png)