import csv
import random
from pymongo import MongoClient

DB_URI    = "URI"
DB_NAME   = "multilingual-language"
CSV_PATH  = "csv/idioms.csv"

LANG_CODE_MAP = {
    "d": "German",
    "s": "Spanish",
    "f": "French",
}

client     = MongoClient(DB_URI)
db         = client[DB_NAME]
languages  = db["languages"]
exercises  = db["exercises"]

def get_language_id(lang_name: str):
    lang = languages.find_one({"name": lang_name})
    if not lang:
        raise ValueError(f"Language '{lang_name}' not found in DB.")
    return lang["_id"]

def import_idioms(csv_path: str):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        print("Detected CSV fields:", reader.fieldnames)

        rows = []
        for raw in reader:
            row = {k.strip().lower(): v for k, v in raw.items() if k is not None}
            idiom     = row.get("idiom")     or row.get("id_idiom")
            definition= row.get("definition")
            example   = row.get("example")
            lang_code = row.get("language")  or row.get("lang")

            if not idiom or not definition or not example or not lang_code:
                print("  ⦻ skipping incomplete row:", row)
                continue

            lang_code = lang_code.strip().lower()
            if lang_code not in LANG_CODE_MAP:
                print(f"  ⦻ skipping unknown language code '{lang_code}'")
                continue

            rows.append({
                "idiom":      idiom.strip(),
                "definition": definition.strip(),
                "example":    example.strip(),
                "lang_code":  lang_code,
            })

    grouped = {}
    for r in rows:
        grouped.setdefault(r["lang_code"], []).append(r)

    for code, group in grouped.items():
        lang_name = LANG_CODE_MAP[code]
        lang_id   = get_language_id(lang_name)
        print(f"\n→ Importing {len(group)} idioms for {lang_name} (lang_id={lang_id})")

        for rec in group:
            pool = [g["idiom"] for g in group if g["idiom"] != rec["idiom"]]
            distractors = random.sample(pool, k=min(3, len(pool)))
            options = distractors + [rec["idiom"]]
            random.shuffle(options)

            doc = {
                "language_id":    lang_id,
                "exercise_type":  "idioms",
                "question":       f"Which idiom means “{rec['definition']}”?",
                "options":        options,
                "correct_answer": rec["idiom"],
                "example":        rec["example"],
                "explanation":    "",
                "source":         "CSV import",
            }
            res = exercises.insert_one(doc)
            print(f"  • inserted _id={res.inserted_id!r}")

    print("\n✅ Finished importing idioms!")

if __name__ == "__main__":
    import_idioms(CSV_PATH)
