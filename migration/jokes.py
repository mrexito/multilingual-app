import csv
from pymongo import MongoClient
from datetime import datetime

DB_URI    = "URI"
DB_NAME   = "multilingual-language"
CSV_PATH  = "csv/jokes.csv"

LANG_CODE_MAP = {
    "d": "German",
    "s": "Spanish",
    "f": "French",
    "e": "English",
}

client    = MongoClient(DB_URI)
db        = client[DB_NAME]
langs     = db["languages"]
jokes_coll = db["jokes"]

def get_language_id(code: str):
    """Lookup the ObjectId in `languages` by code."""
    name = LANG_CODE_MAP.get(code.lower())
    if not name:
        raise ValueError(f"Unknown language code '{code}' in CSV")
    doc = langs.find_one({"name": name})
    if not doc:
        raise ValueError(f"Language '{name}' not found in DB")
    return doc["_id"]

def parse_date(s: str):
    """Turn 'DD.MM.YYYY HH:MM' into a datetime (or None)."""
    s = (s or "").strip()
    for fmt in ("%d.%m.%Y %H:%M", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None

def import_jokes(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for row in reader:
            joke = (row.get("Joke") or "").strip()
            if not joke:
                print("⦻ skipping row w/o a Joke:", row)
                continue

            keywords = []
            for key in ("Word1","Word2","Word3","Word4"):
                w = (row.get(key) or "").strip()
                if w:
                    keywords.append(w)

            try:
                lang_id = get_language_id(row.get("language","").strip())
            except ValueError as e:
                print("⦻", e, "— skipping")
                continue

            def to_int(field):
                val = (row.get(field) or "").replace(",",".").strip()
                return int(float(val)) if val else 0

            def to_float(field):
                val = (row.get(field) or "").replace(",",".").strip()
                return float(val) if val else 0.0

            doc = {
                "keywords":       keywords,
                "joke":           joke,
                "random_number":  to_float("RandomNumber"),
                "counter":        to_int("CounterJokes"),
                "cumul":          to_int("CumulJoke"),
                "date_entry":     parse_date(row.get("DateEntry","")),
                "rf_language":    row.get("RF_Language","").strip(),
                "rf_source":      row.get("RF_Source","").strip(),
                "language_id":    lang_id,
            }

            res = jokes_coll.insert_one(doc)
            print(f"✔ inserted _id={res.inserted_id}")

    print("✅ Done importing jokes.")

if __name__ == "__main__":
    import_jokes(CSV_PATH)
