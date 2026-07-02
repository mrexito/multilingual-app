import csv
from pymongo import MongoClient

DB_URI    = "URI"
DB_NAME   = "multilingual-language"
CSV_PATH  = "csv/spanish/spanishAccent.csv"
LANG_NAME = "Spanish"

client    = MongoClient(DB_URI)
db        = client[DB_NAME]
langs     = db["languages"]
accents   = db["accents"]

lang_doc  = langs.find_one({"name": LANG_NAME})
if not lang_doc:
    raise RuntimeError(f"Language '{LANG_NAME}' not found in `languages` collection")
lang_id = lang_doc["_id"]

def import_accents(csv_path):
    with open(csv_path, encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp, delimiter=";", quotechar='"')
        count = 0

        for row in reader:
            unaccented = row["Palabra"].strip()
            accented   = row["PalabraAcento"].strip() or None
            rule       = row["Code"].strip()
            example    = row.get("Frase", "").strip()

            if not unaccented or not accented:
                print(f"⦻ skipping incomplete entry: {row}")
                continue

            doc = {
                "language_id":   lang_id,
                "unaccented":    unaccented,
                "accented":      accented,
                "rule":     rule,
                "example":       example or None,
            }

            accents.insert_one(doc)
            count += 1

        print(f"✅ imported {count} accent entries.")

if __name__ == "__main__":
    import_accents(CSV_PATH)
