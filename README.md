# Prawnik PL — asystent AI do polskiego prawa i administracji

Prawnik PL powstał podczas prac nad publikacją naukową. To otwarty pakiet instrukcji i narzędzi dla agentów AI, w tym Codex. Pomaga znaleźć i zweryfikować podstawy prawne, obliczać terminy oraz przygotowywać projekty pism. Publiczna beta jest dostępna na licencji MIT.

[Strona projektu i przykłady](https://denis-solodov.github.io/prawnik-pl/) · [English landing page](https://denis-solodov.github.io/prawnik-pl/en/) · [Otwórz SKILL.md](SKILL.md) · [Pobierz ZIP v1.0.0](https://github.com/denis-solodov/prawnik-pl/releases/download/v1.0.0/prawnik-pl-1.0.0.zip) · [O autorach](#o-autorach)

**Wersja:** 1.0.0 (18 listopada 2026 r.)  
**Język:** polski; odpowiada także po angielsku, rosyjsku lub w języku pytania, stosując polskie kategorie prawne.  
**Status:** publiczna beta. Eksperymentalne wsparcie w badaniu prawa i przygotowywaniu projektów pism. W sprawach wymagających porady skorzystaj z pomocy adwokata lub radcy prawnego.

**English** · Prawnik PL is a public beta for Polish law and administration, developed for an upcoming research publication. It uses the [Agent Skills format](https://agentskills.io/specification) to help AI agents verify legal sources, calculate deadlines, and draft documents. You can use it in English while working with Polish law.

[Ogłoszenie UWM](https://uwm.edu.pl/kryminalistyka/ogloszenia/prawnik-pl-publiczna-beta-asystenta-ai-do-prawa-administracji) · [UWM announcement in English](https://uwm.edu.pl/kryminalistyka/en/announcements/prawnik-pl-public-beta-and-invitation-test-ai-skill-polish-law-and-administration)

## Możliwości

- **Materiały referencyjne** porządkują 13 obszarów prawa i wskazują, gdzie szukać przepisów i orzeczeń.
- **Weryfikacja na żywo** wymaga dostępu do internetu. Asystent wskazuje, które podstawy sprawdził w urzędowych źródłach w bieżącej sesji.
- **Kalkulator** działa lokalnie. Wylicza terminy, podstawowe opłaty i odsetki według podanych parametrów oraz sprawdza cyfrę kontrolną NIP.

**Układ pakietu:**

- `SKILL.md` – instrukcje dla agenta i nawigacja;
- `references/area-*.md` – 13 obszarów prawa;
- `references/` – terminy, opłaty, dokumenty, źródła, organy, legalność informacji, weryfikacja firm, kalkulacje i utrzymanie;
- `scripts/legal_calc.py` – kalkulator terminów, standardowych opłat cywilnych, odsetek wg **podanych stawek** i kontrolnej cyfry NIP;
- `scripts/check_data.py` i `data/verified_sources.json` – lokalny test aktualności dat weryfikacji źródeł;
- `tests/` – testy jednostkowe;
- `evals/` – scenariusze do oceny jakości odpowiedzi;
- `agents/openai.yaml` – nazwa, opis i przykładowy prompt w interfejsie.

## Przykłady

- „Dostałem decyzję wojewody 6 listopada 2026 r. Czy mogę się jeszcze odwołać?”
- „Sklep internetowy nie odpowiada na reklamację wadliwego laptopa”.
- „Zwolniono mnie z pracy. Jak obliczyć termin pozwu?”
- „Sprawdź spółkę z o.o. przed podpisaniem umowy – KRS, reprezentacja, KRZ”.
- „Zrób projekt skargi do WSA i wskaż, co muszę dołączyć”.

## Instalacja i użycie

### Instalacja w Codex przez Skills CLI

W folderze projektu uruchom poniższe polecenie. Potrzebujesz Node.js w wersji 22.20 lub nowszej oraz npm.

```bash
npx skills add denis-solodov/prawnik-pl --skill prawnik-pl --agent codex --copy --yes
```

Następnie otwórz ten projekt w Codex i wybierz `$prawnik-pl`.

### Instalacja w Codex z pliku ZIP

1. Pobierz plik ZIP z zakładki Releases i go rozpakuj.
2. Przenieś cały folder pakietu do katalogu projektu tak, aby plik wejściowy znalazł się pod ścieżką `.agents/skills/prawnik-pl/SKILL.md`.
3. Otwórz Codex w tym projekcie i wybierz `$prawnik-pl`. Jeśli skill się nie pojawia, uruchom Codex ponownie.

[Dokumentacja lokalnych skilli w Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

### Instrukcja projektu bez instalacji skilla

Jeśli Twój produkt obsługuje instrukcje i pliki projektu, wklej treść [instrukcji projektu](chatgpt-gemini/INSTRUCTIONS.md) i dodaj potrzebne pliki z `references/`. Możesz też wkleić [krótki prompt](assets/lite_prompt.md) bezpośrednio do rozmowy. Skrypty uruchamiaj lokalnie lub w środowisku, które ma do nich dostęp i obsługuje Python.

## Uruchamianie skryptów

Przykłady korzystają z Python 3.12. W Windows użyj `py -3.12` zamiast `python3`, jeśli masz zainstalowany ten interpreter i launcher. Skrypty nie wymagają dodatkowych bibliotek.

```bash
python3 scripts/legal_calc.py --help
python3 scripts/legal_calc.py deadline --start 2026-12-17 --days 7 --rule kpa
python3 scripts/legal_calc.py courtfee --value 25000
python3 scripts/legal_calc.py interest --principal 10000 --from 2026-11-01 --to 2026-11-18 --annual-rate 9.25
python3 scripts/legal_calc.py nip --number 1234563218
python3 scripts/check_data.py
python3 -m unittest discover -s tests -v
```

## Aktualność prawa

Zestaw zawiera **wybrane** punkty prawne sprawdzone 18.11.2026 w urzędowych źródłach. Inne przepisy są mapą tematyczną i wymagają kontroli w momencie sprawy. Stopy NBP, opłaty sektorowe, terminy szczególne i orzeczenia nie są synchronizowane automatycznie.

## Testy i zgłoszenia

We wstępnych próbach w Codex skill wskazał właściwe podstawy prawne i przygotował pisma dla [trzech fikcyjnych spraw](https://denis-solodov.github.io/prawnik-pl/#examples). Szersza ocena jakości odpowiedzi i niezależna weryfikacja wyników pozostają częścią prac badawczych. [Zestaw ewaluacyjny](evals/README.md) zawiera 20 scenariuszy. Testy automatyczne obejmują wybrane obliczenia i integralność pakietu.

Do testowania zapraszamy prawników, badaczy, studentów prawa i osoby używające agentów AI. Szczególnie przydatne są zgłoszenia błędnie obliczonych terminów, pominiętych wyjątków i rozbieżności z urzędowymi źródłami.

Błędy zgłaszaj przez Issues, a pytania i pomysły przez Discussions. Podaj wersje skilla i modelu, zanonimizowane pytanie oraz odpowiedni fragment odpowiedzi. Usuń dane osobowe i informacje poufne. Szczegóły zawierają [zasady współtworzenia](CONTRIBUTING.md) i [historia zmian](CHANGELOG.md).

<a name="o-autorze"></a>

## O autorach

Projekt prowadzi **dr hab. Denis Solodov, prof. UWM** z Katedry Kryminologii i Kryminalistyki na Wydziale Prawa i Administracji Uniwersytetu Warmińsko-Mazurskiego w Olsztynie. Bada, jak sądy i organy publiczne oceniają dowody i podejmują decyzje przy niepełnych informacjach. Zajmuje się także gwarancjami proceduralnymi oraz wpływem sztucznej inteligencji na podejmowanie decyzji prawnych.

[Profil akademicki Denisa Solodova na stronie UWM](https://www.uwm.edu.pl/kryminalistyka/dr-hab-denis-solodov-prof-uwm) · [ORCID 0000-0003-2884-9420](https://orcid.org/0000-0003-2884-9420)

Współautorem projektu jest **dr Ilia Solodov**, prawnik i specjalista w dziedzinie informatyki śledczej.

## Licencja i autorstwo

Współautorami Prawnik PL są **dr hab. Denis Solodov, prof. UWM** oraz **dr Ilia Solodov**.

Prawnik PL jest udostępniany na [licencji MIT](LICENSE).

Układ pakietu i zestaw 20 scenariuszy ewaluacyjnych zaadaptowano z *Yurist RF 1.2.0* autorstwa **super.biruk64**. Oryginalne wydanie oznaczono jako MIT. Scenariusze, instrukcje i materiały referencyjne dostosowano do prawa polskiego. Kalkulator napisano dla polskich procedur i danych.
