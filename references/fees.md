# Opłaty sądowe i administracyjne — Polska

Weryfikacja punktów odniesienia: 18.11.2026; ustawa o kosztach sądowych w sprawach cywilnych, tekst jednolity Dz.U. 2025 poz. 1228 i zmiana Dz.U. 2025 poz. 1157. **Przed podaniem opłaty do rzeczywistego pisma sprawdź nowelizacje, wyłączenia, rodzaj sprawy, datę wniesienia i zwolnienia**; ustawa rozróżnia setki sytuacji.

## Standardowa opłata od pozwu o prawa majątkowe

Na podstawie art. 13 ust. 1–2 u.k.s.c., gdy **nie ma przepisu szczególnego**, orientacyjnie:

| Wartość przedmiotu sporu (WPS) | Opłata |
| --- | ---: |
| do 500 zł | 30 zł |
| powyżej 500 do 1 500 zł | 100 zł |
| powyżej 1 500 do 4 000 zł | 200 zł |
| powyżej 4 000 do 7 500 zł | 400 zł |
| powyżej 7 500 do 10 000 zł | 500 zł |
| powyżej 10 000 do 15 000 zł | 750 zł |
| powyżej 15 000 do 20 000 zł | 1 000 zł |
| powyżej 20 000 zł | 5% WPS, maks. 100 000 zł |

Zaokrąglaj zgodnie z aktualnym art. 21 u.k.s.c.; przy 5% wartości powyżej 20 tys. skrypt stosuje zaokrąglenie w górę do pełnego złotego. Zmiana limitu ze stanu wcześniejszego (200 000 zł) wynika z nowelizacji z 25.07.2025, obowiązującej od 23.09.2025. Nie przenoś progów opłaty na inne kategorie, np. sprawy gospodarcze w trybach szczególnych, spory bankowe konsumenta (art. 13a), nakazowe, grupowe, WSA/NSA czy rozwód.

## Co jeszcze sprawdzać

- Opłaty stałe dotyczące pozwów rozwodowych, wniosków nieprocesowych, wpisu w księdze wieczystej, środków odwoławczych i skarg.
- Zwolnienia ustawowe, np. przy niektórych sprawach pracowniczych lub konsumenckich, a także limity WPS i szczególne reżimy (art. 96–104 i przepisy szczególne u.k.s.c.). Nie pisz „konsument nie płaci” bez badania sprawy.
- Możliwość zwolnienia od kosztów na wniosek, formularz oświadczenia o stanie rodzinnym/majątku/dochodach, opłata skarbowa od pełnomocnictwa, koszty zastępstwa procesowego.
- WSA/NSA: rozporządzenie dotyczące wpisów i ustawa p.p.s.a.; nie stosuj tabeli opłat KPC.
- Akty notarialne: rozporządzenie o maksymalnych stawkach taksy notarialnej, podatki i opłaty sądowe za wpisy; nie mnoż kwot bez aktualnej tabeli.
- Sprawy administracyjne: ustawa o opłacie skarbowej wraz z załącznikiem i zwolnieniami; sprawdź organ właściwy do zapłaty.

## Weryfikacja kwoty

1. Zidentyfikuj pismo i tryb (pozew, wniosek, apelacja, sprzeciw, skarga) oraz strony.
2. Wylicz WPS zgodnie z odpowiednimi przepisami KPC i sprawdź zwolnienie.
3. Zweryfikuj art. 13 i szczególny artykuł u.k.s.c. według stanu na datę złożenia.
4. Dla standardowej opłaty użyj `python3 scripts/legal_calc.py courtfee --value 50000` i opisz założenia.
5. Podaj rachunek do wpłaty wyłącznie po identyfikacji właściwego sądu z jego **oficjalnej** strony.
