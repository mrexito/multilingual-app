import json
from pymongo import MongoClient

db_uri = "URI"
client = MongoClient(db_uri)

database = client["multilingual-language"]
words_collection = database["words"]
languages_collection = database["languages"]

def get_language_id(language_name):
    doc = languages_collection.find_one({"name": language_name})
    if doc:
        return doc["_id"]
    else:
        raise ValueError(f"Language '{language_name}' not found in 'languages' collection.")

LANGUAGE_MAP = {
    "german": "German",
    "spanish": "Spanish",
    "english": "English"
}

def add_translations(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        word_text = entry.get("word")
        if not word_text:
            print("No 'word' field, skipping:", entry)
            continue
        
        word_doc = words_collection.find_one({"word": word_text})
        if not word_doc:
            print(f"Could not find word '{word_text}' in the DB. Skipping.")
            continue

        translations_list = []
        for key, value in entry.items():
            if key.lower() == "word":
                continue
            if not value:
                continue
            
            if key.lower() in LANGUAGE_MAP:
                lang_name = LANGUAGE_MAP[key.lower()]
                try:
                    lang_id = get_language_id(lang_name)
                except ValueError as e:
                    print(e)
                    continue
                
                translations_list.append({
                    "language_id": lang_id,
                    "translation": value
                })
            else:
                pass

        if not translations_list:
            print(f"No translations found for '{word_text}'—maybe all fields were empty?")
            continue
        words_collection.update_one(
            {"_id": word_doc["_id"]},
            {"$push": {"translations": {"$each": translations_list}}}
        )

        print(f"Updated '{word_text}' with {len(translations_list)} translations.")

if __name__ == "__main__":
    json_path = "translations/italianWordsWithoutTrans.json"
    add_translations(json_path)
