# Scenariusze ewaluacyjne Prawnik PL 1.0

Zestaw odzwierciedla dwadzieścia typów zadań z załączonego wzorca Yurist RF, lecz z **polskimi** przepisami i organami. Każdy folder zawiera `prompt.md` (przykładowe pytanie użytkownika) i `criteria.md` (kryteria dobrej odpowiedzi).

**Zasady wspólne:** weryfikacja aktualnego prawa (lub jawne oznaczenie braku weryfikacji), właściwa procedura i organ, nieprzekraczanie biegnących terminów, brak zmyślonych artykułów i sygnatur, brak pewnych deklaracji o wyniku, poszanowanie danych osobowych i bezpieczeństwa. Przypadki są narzędziami kontroli jakości, nie poradą prawną.

## Jak sprawdzać

1. Zainstaluj pakiet zgodnie z [README](../README.md). Przy standardowym przebiegu model korzysta z `SKILL.md` i otwiera materiały potrzebne do sprawy. Zapisz też dostępność przeglądania i uruchamiania skryptów.
2. Otwórz nową rozmowę dla każdego przypadku i podaj treść `prompt.md`. W przypadku `20-multiturn-dismissal` wyślij kolejne wiadomości w tej samej rozmowie.
3. Porównaj odpowiedź z `criteria.md`. Osoba oceniająca sprawdza podstawy w urzędowych źródłach według właściwego stanu prawnego.
4. W wynikach podaj wersję skilla, model i jego wersję, datę, tryb, dostępność narzędzi, osobę oceniającą oraz wyniki i uchybienia dla każdego przypadku.
5. Jeśli udostępnisz modelowi wszystkie pliki referencyjne od razu, oznacz taki przebieg jako test pełnego kontekstu.

Dotychczas nie opublikowano wyników modelowych dla Prawnik PL 1.0.0.
