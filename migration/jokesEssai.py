#!/usr/bin/env python3
# import_jokes.py

import csv
from pymongo import MongoClient
from datetime import datetime

DB_URI    = "URI"
DB_NAME   = "multilingual-language"

client     = MongoClient(DB_URI)
db         = client[DB_NAME]
langs      = db["languages"]
jokes_coll = db["jokes"]


LANG_CODE_MAP = {
    "d": "German",
    "s": "Spanish",
    "f": "French",
    "e": "English",
}


def get_language_id(code: str):
    """Lookup the ObjectId for a one‐letter language code."""
    name = LANG_CODE_MAP.get(code.lower())
    if not name:
        raise ValueError(f"Unknown language code '{code}'")
    lang = langs.find_one({"name": name})
    if not lang:
        raise ValueError(f"Language '{name}' not found in languages collection")
    return lang["_id"]


def parse_date(s: str):
    """Try a couple of common formats; return a Python datetime or None."""
    for fmt in ("%d.%m.%Y %H:%M", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def normalize_row(raw: dict):
    """
    Lower‐case all incoming keys and pull out:
      - Nr           → skip
      - RandomNumber → random_number
      - language     → lang_code
      - Word1–4      → keywords[]
      - Joke         → joke
      - RF_Source    → rf_source
      - CounterJokes → counter
      - CumulJoke    → cumul
      - DateEntry    → date_entry
      - Source       → source
    """
    L = {k.strip().lower(): v.strip() for k, v in raw.items()}

    return {
        "random_number": int(L.get("randomnumber", 0) or 0),
        "lang_code":     L.get("language", ""),
        "keywords":      [L.get(f"word{i}", "") for i in (1, 2, 3, 4) if L.get(f"word{i}", "")],
        "joke":          L.get("joke", ""),
        "rf_source":     L.get("rf_source", ""),
        "counter":       int(L.get("counterjokes", 0) or 0),
        "cumul":         int(L.get("cumuljoke", 0) or 0),
        "date_entry":    L.get("dateentry", ""),
        "source":        L.get("source", ""),
    }


def import_jokes(csv_path: str):
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for raw in reader:
            row = normalize_row(raw)

            if not row["joke"]:
                print("⦻ no joke, skipping row:", raw)
                continue

            try:
                lang_id = get_language_id(row["lang_code"])
            except ValueError as e:
                print("⦻", e, "— skipping")
                continue

            dt = parse_date(row["date_entry"])
            if dt is None:
                print("⚠️ invalid date:", row["date_entry"], "; saving null")

            doc = {
                "keywords":      row["keywords"],
                "joke":          row["joke"],
                "random_number": row["random_number"],
                "counter":       row["counter"],
                "cumul":         row["cumul"],
                "date_entry":    dt,
                "rf_source":     row["rf_source"],
                "source":        row["source"],
                "language_id":   lang_id,
            }

            res = jokes_coll.insert_one(doc)
            print(f"✔ inserted joke _id={res.inserted_id}")

    print("✅ Finished importing jokes.")


if __name__ == "__main__":
    import_jokes("csv/jokes.csv")
