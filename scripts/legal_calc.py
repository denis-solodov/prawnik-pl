#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prawnik PL: arytmetyka terminow, standardowych oplat, odsetek i NIP.

Python >=3.9; no external dependencies or network. This is a calculation aid,
not a legal determination. Read ../references/calculators.md and current statutes.
Law review reference date: 2026-11-18.
"""
from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP

D = Decimal
PLN = D("0.01")
RULES = ("kpa", "kc", "kpc", "ppsa", "tax", "none")
SOURCE_FEE = "ustawa o kosztach sadowych w sprawach cywilnych art. 13; Dz.U. 2025 poz. 1228 i 1157"
SOURCE_DAYS = "ustawa o dniach wolnych od pracy (Dz.U. 2025 poz. 296)"


class CalcError(ValueError):
    pass


def parse_date(raw: str) -> date:
    raw = raw.strip()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            return date.fromisoformat(raw)
        if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", raw):
            day, month, year = map(int, raw.split("."))
            return date(year, month, day)
    except ValueError as exc:
        raise CalcError(f"Nieistniejaca data: {raw}") from exc
    raise CalcError(f"Data musi miec format RRRR-MM-DD lub DD.MM.RRRR: {raw}")


def dec(raw: object, *, strictly_positive: bool = True) -> Decimal:
    try:
        value = D(str(raw).replace(" ", "").replace(",", "."))
    except (InvalidOperation, ValueError) as exc:
        raise CalcError(f"Niepoprawna liczba: {raw}") from exc
    if not value.is_finite() or value < 0 or (strictly_positive and value == 0):
        raise CalcError(f"Liczba musi byc {'dodatnia' if strictly_positive else 'nieujemna'}: {raw}")
    return value


def round_pln(v: Decimal) -> Decimal:
    return v.quantize(PLN, rounding=ROUND_HALF_UP)


def easter_sunday(year: int) -> date:
    """Meeus/Jones/Butcher Gregorian computus."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451
    month = (h + L - 7 * m + 114) // 31
    day = (h + L - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def statutory_holidays(year: int) -> set[date]:
    fixed = [(1, 1), (1, 6), (5, 1), (5, 3), (8, 15), (11, 1),
             (11, 11), (12, 25), (12, 26)]
    # Statutory Christmas Eve holiday was introduced from 2025-02-01.
    if year >= 2025:
        fixed.append((12, 24))
    # Epiphany was restored as a statutory holiday in 2011.
    if year < 2011:
        fixed.remove((1, 6))
    easter = easter_sunday(year)
    return ({date(year, m, d) for m, d in fixed}
            | {easter, easter + timedelta(days=1), easter + timedelta(days=49),
               easter + timedelta(days=60)})


def is_weekend_or_holiday(dt: date) -> bool:
    return dt.weekday() >= 5 or dt in statutory_holidays(dt.year)


def add_months(dt: date, count: int) -> date:
    index = (dt.month - 1) + count
    year = dt.year + index // 12
    month = index % 12 + 1
    return date(year, month, min(dt.day, calendar.monthrange(year, month)[1]))


def calculate_deadline(start: date, count: int, unit: str, rule: str) -> dict:
    if count <= 0:
        raise CalcError("Liczba jednostek czasu musi byc dodatnia")
    if rule not in RULES:
        raise CalcError("Nieznany rodzaj procedury")
    if unit == "days":
        raw_end = start + timedelta(days=count)
    elif unit == "weeks":
        raw_end = start + timedelta(days=7 * count)
    elif unit == "months":
        raw_end = add_months(start, count)
    elif unit == "years":
        raw_end = add_months(start, 12 * count)
    else:
        raise CalcError("Nieznana jednostka")
    final = raw_end
    if rule != "none":
        while is_weekend_or_holiday(final):
            final += timedelta(days=1)
    return {
        "operation": "deadline", "event_date": start.isoformat(), "unit": unit,
        "count": count, "rule": rule, "calendar_end": raw_end.isoformat(),
        "last_day": final.isoformat(), "shifted": final != raw_end,
        "warning": ("Orientacyjnie: ustal w prawie wlasciwy poczatek, wyjatki, "
                    "przepisy przejsciowe oraz sposob skutecznego wniesienia. "
                    "Dni uznane za wolne z przyczyn miejscowych nie sa modelowane."),
        "holiday_source": SOURCE_DAYS,
    }


def calculate_courtfee(value: Decimal) -> dict:
    if value <= 0:
        raise CalcError("WPS musi byc dodatni")
    thresholds = ((D(500), 30), (D(1500), 100), (D(4000), 200),
                  (D(7500), 400), (D(10000), 500), (D(15000), 750),
                  (D(20000), 1000))
    if value <= D(20000):
        fee = next(fee for limit, fee in thresholds if value <= limit)
        amount = D(fee)
        mode = "fixed_bracket"
    else:
        amount = min((value * D("0.05")).to_integral_value(rounding=ROUND_CEILING),
                     D(100000))
        mode = "5_percent_capped"
    return {
        "operation": "courtfee", "value_pln": f"{round_pln(value):.2f}",
        "fee_pln": f"{amount:.2f}", "method": mode, "source": SOURCE_FEE,
        "warning": ("Tylko standardowa oplata art. 13 u.k.s.c. dla spraw o prawa "
                    "majatkowe bez wyjatkow/zwolnien. Zweryfikuj aktualny stan, "
                    "rodzaj pisma, tryb i date jego wniesienia."),
    }


def calculate_days(begin: date, end: date) -> dict:
    if end < begin:
        raise CalcError("Data do nie moze byc wczesniejsza od daty od")
    difference = (end - begin).days
    return {"operation": "days", "from": begin.isoformat(), "to": end.isoformat(),
            "difference_excluding_start": difference, "inclusive_days": difference + 1}


def calculate_interest(principal: Decimal, begin: date, end: date,
                       rate: Decimal | None, segments: list[tuple[date, date, Decimal]]) -> dict:
    if end < begin:
        raise CalcError("Koniec okresu musi byc nie wczesniej niz poczatek")
    if rate is not None and segments:
        raise CalcError("Podaj albo --annual-rate, albo --segment; nie oba")
    if rate is None and not segments:
        raise CalcError("Musisz podac --annual-rate albo przynajmniej jeden --segment")
    if rate is not None:
        segments = [(begin, end, rate)]
    segments = sorted(segments, key=lambda x: x[0])
    cursor = begin
    details = []
    total = D(0)
    for start, stop, annual in segments:
        if start != cursor:
            raise CalcError(f"Luka lub nakladanie okresow w dniu {cursor.isoformat()}")
        if stop < start or stop > end:
            raise CalcError("Niepoprawny przedzial odsetek")
        days = (stop - start).days + 1  # dates are expressly inclusive
        raw = principal * annual / D(100) * D(days) / D(365)
        details.append({"from": start.isoformat(), "to": stop.isoformat(),
                        "days_inclusive": days, "annual_percent": str(annual),
                        "interest_unrounded_pln": str(raw)})
        total += raw
        cursor = stop + timedelta(days=1)
    if cursor != end + timedelta(days=1):
        raise CalcError(f"Niepokryty okres od {cursor.isoformat()}")
    return {"operation": "interest", "principal_pln": f"{round_pln(principal):.2f}",
            "from_inclusive": begin.isoformat(), "to_inclusive": end.isoformat(),
            "year_basis_days": 365, "segments": details,
            "total_interest_pln": f"{round_pln(total):.2f}",
            "warning": ("To obliczenie matematyczne wedlug jawnie podanych rocznych stawek, "
                        "nie aktualny kurs/stawka pobrana z NBP. Sam ustal prawidlowe daty, "
                        "stawki, wyjatki i podstawe prawna; nie dotyczy automatycznie "
                        "odsetek podatkowych ani handlowych."),
            }


def check_nip(number: str) -> dict:
    cleaned = re.sub(r"[\s-]", "", number)
    if not re.fullmatch(r"\d{10}", cleaned):
        raise CalcError("NIP musi skladac sie z 10 cyfr (pomijajac spacje i '-')")
    nums = [int(ch) for ch in cleaned]
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    control = sum(i * w for i, w in zip(nums[:9], weights)) % 11
    valid = control != 10 and control == nums[9]
    return {"operation": "nip", "number": cleaned,
            "checksum_valid": valid, "expected_control_digit": control if control != 10 else None,
            "warning": "Sprawdzenie samej sumy kontrolnej nie potwierdza nadania NIP ani tozsamosci podmiotu."}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="Wynik JSON (moze byc tez po komendzie)")
    subs = p.add_subparsers(dest="operation", required=True)
    deadline = subs.add_parser("deadline", help="Termin procesowy / materialny (po sprawdzeniu prawa)")
    deadline.add_argument("--start", required=True, help="Data zdarzenia RRRR-MM-DD")
    g = deadline.add_mutually_exclusive_group(required=True)
    g.add_argument("--days", type=int)
    g.add_argument("--weeks", type=int)
    g.add_argument("--months", type=int)
    g.add_argument("--years", type=int)
    deadline.add_argument("--rule", required=True, choices=RULES, help="Tryb liczenia sobot i swiat")

    fee = subs.add_parser("courtfee", help="Standardowa oplata art.13 u.k.s.c.")
    fee.add_argument("--value", required=True, help="WPS w PLN")

    interest = subs.add_parser("interest", help="Odsetki wedlug jawnych stawek rocznych")
    interest.add_argument("--principal", required=True)
    interest.add_argument("--from", dest="from_date", required=True)
    interest.add_argument("--to", dest="to_date", required=True)
    interest.add_argument("--annual-rate", help="Roczna stopa %% w podanym okresie")
    interest.add_argument("--segment", nargs=3, action="append", metavar=("FROM", "TO", "RATE"), default=[])

    days = subs.add_parser("days", help="Roznica dni i wariant inkluzywny")
    days.add_argument("--from", dest="from_date", required=True)
    days.add_argument("--to", dest="to_date", required=True)

    nip = subs.add_parser("nip", help="Kontrola sumy NIP")
    nip.add_argument("--number", required=True)
    return p


def run(args: argparse.Namespace) -> dict:
    if args.operation == "deadline":
        unit, number = next((u, getattr(args, u)) for u in ("days", "weeks", "months", "years")
                            if getattr(args, u) is not None)
        return calculate_deadline(parse_date(args.start), number, unit, args.rule)
    if args.operation == "courtfee":
        return calculate_courtfee(dec(args.value))
    if args.operation == "days":
        return calculate_days(parse_date(args.from_date), parse_date(args.to_date))
    if args.operation == "interest":
        segs = [(parse_date(a), parse_date(b), dec(c, strictly_positive=False))
                for a, b, c in args.segment]
        return calculate_interest(dec(args.principal), parse_date(args.from_date),
                                  parse_date(args.to_date),
                                  dec(args.annual_rate, strictly_positive=False)
                                  if args.annual_rate is not None else None, segs)
    if args.operation == "nip":
        return check_nip(args.number)
    raise CalcError("Nieznana operacja")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except (CalcError, OverflowError, ValueError) as exc:
        if as_json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"Blad: {exc}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
