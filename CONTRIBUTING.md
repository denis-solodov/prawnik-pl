# Współtworzenie Prawnik PL

Zgłaszaj błędy prawne, błędy kalkulatora, problemy z instalacją i braki w zakresie skilla przez **Issues**. Pytania, pomysły i zanonimizowane wrażenia z użycia kieruj do **Discussions**.

Przed publikacją zgłoszenia usuń dane osobowe, identyfikatory sprawy, poufne informacje i dokumenty. Najłatwiej odtworzyć błąd na krótkim, fikcyjnym przykładzie.

## Poprawki prawne

Dołącz link do właściwego aktu lub orzeczenia z urzędowego źródła, jednostkę redakcyjną lub sygnaturę i datę właściwego stanu prawnego. Opisz, jak przepis zmienia odpowiedź. Podaj przykład, który pozwoli wykryć ten sam błąd po kolejnej zmianie, np. scenariusz z kryteriami w `evals/` albo test kalkulatora.

## Pull requesty

Otwórz pull request z opisem zmiany i sposobem jej sprawdzenia. Przed scaleniem sprawdź wyniki testów i uwagi recenzenta. Daty przeglądu podstaw prawnych zmieniaj tylko dla faktycznie zweryfikowanych pozycji.

```bash
python -B -m unittest discover -s tests -v
python -B scripts/check_data.py
```

Druga komenda sprawdza daty zapisanych weryfikacji. Dla poprawki prawnej sprawdź też źródło urzędowe.
