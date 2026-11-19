#!/usr/bin/env python3
"""Offline validation of source review dates in Prawnik PL.

This does not verify whether official websites contain current law. That step
requires live legal research at the moment of consultation.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", default=date.today().isoformat())
    args = parser.parse_args(argv)
    today = date.fromisoformat(args.today)
    dataset = json.loads((ROOT / "data" / "verified_sources.json").read_text(encoding="utf-8"))
    max_age = int(dataset["meta"]["review_after_days"])
    errors = []
    ids = set()
    for obj in dataset["sources"]:
        key = obj["id"]
        if key in ids:
            errors.append(f"Duplicate id: {key}")
        ids.add(key)
        dt = date.fromisoformat(obj["checked"])
        if dt > today:
            errors.append(f"{key}: checked date in the future")
        elif (today - dt).days > max_age:
            errors.append(f"{key}: last review {dt} exceeds {max_age} days")
        if not obj["url"].startswith("https://"):
            errors.append(f"{key}: missing HTTPS source")
    meta_dt = date.fromisoformat(dataset["meta"]["last_reviewed"])
    if meta_dt > today:
        errors.append("meta.last_reviewed in future")
    if len(dataset["sources"]) < 1:
        errors.append("No source records")
    if errors:
        for err in errors:
            print("ALERT:", err)
        return 1
    print(f"OK: {len(ids)} provenance entries within {max_age} days, today {today}.")
    print("Reminder: source freshness is not live verification of any statute.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
