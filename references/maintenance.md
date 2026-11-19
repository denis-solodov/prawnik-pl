# Utrzymanie i audyt aktualności

1. Co najmniej raz na 30 dni sprawdzaj `data/verified_sources.json` i aktualizuj wyłącznie te rekordy, które **rzeczywiście** zweryfikowano w pierwotnym źródle, z datą i linkiem. Uruchom `python3 scripts/check_data.py`.
2. Każda zmiana prawa może zmienić termin, opłatę, właściwość lub tryb: sprawdzaj akty zmieniające po ostatnim tekście jednolitym, przepisy przejściowe, vacatio legis i projekty **nie** traktuj jako obowiązujące prawo.
3. Szczególnie monitoruj: e-Doręczenia, cyfryzację sądów, przepisy migracyjne/Pakt UE, zmiany konsumenckie i bankowe, stopy NBP/MF, koszty sądowe, Kodeks pracy, podatki i terminy roczne.
4. Skrypt kalkulacyjny nie może automatycznie zakładać bieżącej stopy NBP. Jego prawidłowość matematyczna jest osobnym zagadnieniem od prawidłowości normatywnej stawki.
5. Weryfikuj nazwy organów i URL-e, zmieniające się systemy elektroniczne i drogi odwoławcze.
6. Po zmianach uruchom `python3 -m unittest discover -s tests -v`; następnie przeczytaj scenariusze z `evals/`, dopasuj oczekiwany wynik do aktualnego prawa i przetestuj na rzeczywistym modelu.
7. Każdą niezweryfikowaną kwotę lub termin oznacz jawnie w odpowiedzi jako wymagającą potwierdzenia. Nie aktualizuj daty `checked` przez sam fakt edycji pliku.

## Status wersji

Wydanie początkowe: 18.11.2026. Materiały referencyjne są **mapą zagadnień i źródeł**, nie bazą aktów prawnych w pełnym brzmieniu. Przed praktycznym użyciem obowiązkowa weryfikacja normy w aktualnej wersji.
