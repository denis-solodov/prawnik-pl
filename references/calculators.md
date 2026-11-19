# Obliczenia — termin, koszty, odsetki i NIP

**Używaj w zestawieniu z ustawą, nie zamiast ustawy.** `scripts/legal_calc.py` (Python >=3.9, standard library) nie korzysta z Internetu. Obliczenia są arytmetyczne i nie przesądzają, od jakiej daty dane świadczenie jest należne.

## Termin

`python3 scripts/legal_calc.py deadline --start 2026-11-18 --days 14 --rule kpa`

`python3 scripts/legal_calc.py deadline --start 2026-01-31 --months 1 --rule kpa`

`python3 scripts/legal_calc.py deadline --start 2026-12-24 --weeks 2 --rule kc`

- `--start`: dzień zdarzenia, np. doręczenia. `--days/--weeks/--months/--years`: jednostka.
- `--rule`: `kpa`, `kc`, `kpc`, `ppsa`, `tax`, `none`. KPC odsyła do KC w sprawach liczenia terminu; inne tryby mogą wymagać dodatkowych regulacji.
- W trybach `kpa/kc/kpc/ppsa/tax` ostatni dzień będący sobotą, niedzielą lub świętem z ustawy z 1951 r. jest przesuwany. `none` nie przesuwa. Prawdziwość takiej reguły **dla konkretnego terminu** zawsze sprawdzaj w prawie.
- Wyliczenie dotyczy kalendarza ogólnokrajowego; święta nadzwyczajne, okresy zawieszeń, szczególne ustawy oraz godziny urzędowania są wyłączone.

## Standardowa opłata sądowa

`python3 scripts/legal_calc.py courtfee --value 25000`

Tylko standardowe pismo dotyczące prawa majątkowego, niezwolnione z opłaty (u.k.s.c. art. 13). Nie stosuj automatycznie w sprawach konsumenckich, pracowniczych, bankowych, sądowoadministracyjnych, przy skardze lub w trybie nakazowym.

## Odsetki

`python3 scripts/legal_calc.py interest --principal 10000 --from 2026-11-01 --to 2026-11-18 --annual-rate 9.25`

`python3 scripts/legal_calc.py interest --principal 10000 --from 2026-01-01 --to 2026-03-31 --segment 2026-01-01 2026-02-15 10.0 --segment 2026-02-16 2026-03-31 9.5`

Parametr `--annual-rate` oznacza **podaną przez użytkownika lub zweryfikowaną stawkę**, a nie aktualną stopę NBP. `--segment` daje kontrolowane przedziały. Skrypt liczy dni włącznie z datami `--from` i `--to`; to użytkownik/analizujący musi ustalić rzeczywisty pierwszy i ostatni dzień naliczania. Przy zmiennych stopach do wyliczenia polskich odsetek ustawowych zwykłych (KC art. 359) lub za opóźnienie (KC art. 481) potrzebne są odpowiednio stawka referencyjna NBP +3,5 albo +5,5 pkt proc. i prawidłowe okresy obowiązywania. Ustawa o przeciwdziałaniu nadmiernym opóźnieniom w transakcjach handlowych przewiduje **inne** zasady, których ta funkcja nie implementuje.

Skrypt pokazuje mianownik 365 dni i zaokrąglenie; przy znaczących kwotach i nietypowym okresie potwierdź metodę w źródle i praktyce stosowania. Nie oblicza odsetek maksymalnych, kapitałowych, składanych ani biegu przedawnienia.

## Inne

- `python3 scripts/legal_calc.py days --from 2026-11-01 --to 2026-11-18` – różnica dni i wariant włącznie.
- `python3 scripts/legal_calc.py nip --number 1234563218` – kontrolna cyfra polskiego NIP (tylko **format/checksum**, nie identyfikuje przedsiębiorcy).
- Flaga `--json` (przed lub po podkomendzie) zwraca dane maszynowe.
- `python3 scripts/check_data.py` – ostrzega, jeżeli metryka ostatniej weryfikacji wymaga aktualizacji.
