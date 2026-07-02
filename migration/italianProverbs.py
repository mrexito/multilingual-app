import csv
from pymongo import MongoClient
from datetime import datetime

DB_URI    = "URI"
DB_NAME   = "multilingual-language"

CSV_PATH  = "csv/italian/italianProverb.csv"

LANG_MAP  = {
    "Italian":  "Italian",
    "it":       "Italian",
    "italian":  "Italian",
}

client     = MongoClient(DB_URI)
db         = client[DB_NAME]
langs      = db["languages"]
proverbs   = db["proverbs"]


def get_language_id(name_or_code: str):
    key = LANG_MAP.get(name_or_code.strip(), None)
    if not key:
        raise ValueError(f"Unknown language key '{name_or_code}'")
    doc = langs.find_one({"name": key})
    if not doc:
        raise ValueError(f"Language '{key}' not in languages collection")
    return doc["_id"]


def parse_date(s: str):
    for fmt in ("%d.%m.%Y %H:%M:%S", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None


def import_proverbs(csv_path):
    lang_id = get_language_id("Italian")
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for row in reader:
            proverb    = row.get("Proverb","").strip().strip('"')
            definition = row.get("Definition","").strip().strip('"')
            tema       = row.get("Tema","").strip().strip('"') or None
            w1         = row.get("Word1","").strip().strip('"')
            w2         = row.get("Word2","").strip().strip('"')
            trans_f    = row.get("Translation_F","").strip().strip('"')
            trans_gb   = row.get("Translation_GB","").strip().strip('"')
            date_raw   = row.get("DateEntry","").strip().strip('"')
            rnd        = int(row.get("RandomNumber","0") or 0)
            counter    = int(row.get("Counter","0") or 0)
            cumul      = int(row.get("Cumul","0") or 0)

            if not proverb:
                print("⦻ missing proverb, skipping row:", row)
                continue

            dt = parse_date(date_raw)
            if dt is None:
                print("⚠️ couldn't parse date:", date_raw)

            doc = {
                "language_id":  lang_id,
                "proverb":      proverb,
                "definition":   definition,
                "tema":         tema,
                "keywords":     [k for k in (w1,w2) if k],
                "translations": {
                    "fr": trans_f or None,
                    "en": trans_gb or None,
                },
                "date_entry":   dt,
                "random_number":rnd,
                "counter":      counter,
                "cumul":        cumul,
            }

            res = proverbs.insert_one(doc)
            print(f"✔ imported proverb _id={res.inserted_id}")

    print("✅ Done importing proverbs.")


if __name__ == "__main__":
    import_proverbs(CSV_PATH)
