import json
from pymongo import MongoClient
from datetime import datetime

DB_URI     = "URI"
DB_NAME    = "multilingual-language"
JSON_PATH  = "json/spanishConjugations.json"
LANG_NAME  = "Spanish"

client     = MongoClient(DB_URI)
db         = client[DB_NAME]
languages  = db["languages"]
conj_coll  = db["conjugations"]

lang_doc = languages.find_one({"name": LANG_NAME})
if not lang_doc:
    raise RuntimeError(f"Language '{LANG_NAME}' not found in `languages` collection")
lang_id = lang_doc["_id"]

def import_conjugations(json_path: str):
    inserted = 0
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        forms = entry.get("forms", [])
        if len(forms) != 6:
            print(f"⚠️  skipping verb_id={entry.get('verb_id')} – expected 6 forms, got {len(forms)}")
            continue

        doc = {
            "language_id": lang_id,
            "verb_id":     entry["verb_id"],
            "tense":       entry["tense"],
            "forms":       forms,
            "date_entry":  datetime.fromisoformat(entry["date_entry"]["$date"].replace("Z", "+00:00")),
            "cumul":       int(entry.get("cumul", 0)),
            "counter":     int(entry.get("counter", 0)),
            "infinitive":  entry.get("infinitive")
        }

        conj_coll.insert_one(doc)
        inserted += 1

    print(f"✅ Imported {inserted} conjugation entries from JSON.")

if __name__ == "__main__":
    import_conjugations(JSON_PATH)
