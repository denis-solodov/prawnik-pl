"""Deterministic tests; legal assumptions still require current-source review."""
import importlib.util
import json
import subprocess
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "legal_calc.py"
spec = importlib.util.spec_from_file_location("pllegalcalc", SCRIPT)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


class LegalCalcTests(unittest.TestCase):
    def test_holidays_movable_and_fixed(self):
        h = calc.statutory_holidays(2026)
        self.assertIn(date(2026, 4, 5), h)   # Easter
        self.assertIn(date(2026, 4, 6), h)   # Easter Monday
        self.assertIn(date(2026, 6, 4), h)   # Corpus Christi
        self.assertIn(date(2026, 12, 24), h) # Christmas Eve
        self.assertNotIn(date(2026, 11, 30), h)
        self.assertNotIn(date(2024, 12, 24), calc.statutory_holidays(2024))
        self.assertNotIn(date(2010, 1, 6), calc.statutory_holidays(2010))

    def test_kpa_weekend_shift(self):
        x = calc.calculate_deadline(date(2026, 11, 27), 1, "days", "kpa")
        self.assertEqual(x["calendar_end"], "2026-11-28")
        self.assertEqual(x["last_day"], "2026-11-30")

    def test_christmas_eve_shift(self):
        x = calc.calculate_deadline(date(2026, 12, 17), 7, "days", "kpa")
        self.assertEqual(x["last_day"], "2026-12-28")

    def test_no_shift_when_none(self):
        x = calc.calculate_deadline(date(2026, 12, 17), 7, "days", "none")
        self.assertEqual(x["last_day"], "2026-12-24")

    def test_month_february_and_weekend(self):
        x = calc.calculate_deadline(date(2026, 1, 31), 1, "months", "kpa")
        self.assertEqual(x["calendar_end"], "2026-02-28")
        self.assertEqual(x["last_day"], "2026-03-02")

    def test_leap_day_to_non_leap_year(self):
        x = calc.calculate_deadline(date(2024, 2, 29), 1, "years", "none")
        self.assertEqual(x["calendar_end"], "2025-02-28")

    def test_court_fees_boundaries(self):
        expected = {"500": "30.00", "501": "100.00", "1500": "100.00",
                    "1501": "200.00", "20000": "1000.00", "20001": "1001.00",
                    "25000": "1250.00", "2000000": "100000.00", "3000000": "100000.00"}
        for value, fee in expected.items():
            with self.subTest(value=value):
                self.assertEqual(calc.calculate_courtfee(Decimal(value))["fee_pln"], fee)

    def test_interest_basic(self):
        x = calc.calculate_interest(Decimal("36500"), date(2026, 1, 1),
                                    date(2026, 1, 10), Decimal("10"), [])
        self.assertEqual(x["total_interest_pln"], "100.00")
        self.assertEqual(x["segments"][0]["days_inclusive"], 10)

    def test_interest_segments_cover(self):
        a = (date(2026, 1, 1), date(2026, 1, 5), Decimal("10"))
        b = (date(2026, 1, 6), date(2026, 1, 10), Decimal("10"))
        x = calc.calculate_interest(Decimal("36500"), date(2026, 1, 1),
                                    date(2026, 1, 10), None, [b, a])
        self.assertEqual(x["total_interest_pln"], "100.00")

    def test_interest_rejects_gap_or_overlap(self):
        with self.assertRaises(calc.CalcError):
            calc.calculate_interest(Decimal("1000"), date(2026, 1, 1),
                                    date(2026, 1, 10), None,
                                    [(date(2026, 1, 1), date(2026, 1, 5), Decimal("10")),
                                     (date(2026, 1, 7), date(2026, 1, 10), Decimal("10"))])

    def test_nip(self):
        self.assertTrue(calc.check_nip("123-456-32-18")["checksum_valid"])
        self.assertFalse(calc.check_nip("1234563219")["checksum_valid"])
        with self.assertRaises(calc.CalcError):
            calc.check_nip("123456789")

    def test_json_after_operation(self):
        out = subprocess.run([sys.executable, str(SCRIPT), "nip", "--number", "1234563218", "--json"],
                             text=True, check=True, capture_output=True)
        self.assertTrue(json.loads(out.stdout)["ok"])

    def test_negative_amount_rejected(self):
        with self.assertRaises(calc.CalcError):
            calc.calculate_courtfee(Decimal("-100"))


if __name__ == "__main__":
    unittest.main()
