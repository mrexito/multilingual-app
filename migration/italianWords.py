import csv
from pymongo import MongoClient

db_uri = "URI"
client = MongoClient(db_uri)

database = client["multilingual-language"]
words_collection = database["words"]
languages_collection = database["languages"]

def get_language_id(language_name: str):
    doc = languages_collection.find_one({"name": language_name})
    if not doc:
        raise ValueError(f"Language '{language_name}' not found in 'languages' collection.")
    return doc["_id"]

def import_italian_words(csv_path: str):
    italian_language_id = get_language_id("Italian")
    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(
            csvfile,
            delimiter=';',
            quotechar='"',
            fieldnames=[
                "ID_Word_I", "Word", "TypeOfWord", "Artikel_ref",
                "Nature_ref", "Sentence", "F_translation",
                "DateEntryWord", "DateSource", "Source_ref",
                "TitleOfArticle", "Definition_I", "RandomNumber",
                "CounterWord", "CumulWord", "Gramm"
            ]
        )

        for row in reader:
            word_text = row["Word"] or ""
            if not word_text.strip():
                continue

            doc = {
                "language_id": italian_language_id,
                "word": word_text.strip(),
                "type": row["TypeOfWord"] or "",
                "front_text": row["Sentence"] or "",
                "definition": row["Definition_I"] or "",
                "additional_info": {
                    "artikel_ref": row["Artikel_ref"] or "",
                    "nature_ref": row["Nature_ref"] or "",
                    "date_entry_word": row["DateEntryWord"] or "",
                    "date_source": row["DateSource"] or "",
                    "source_ref": row["Source_ref"] or "",
                    "title_of_article": row["TitleOfArticle"] or "",
                    "random_number": row["RandomNumber"] or "",
                    "counter_word": row["CounterWord"] or "",
                    "cumul_word": row["CumulWord"] or "",
                    "gramm": row["Gramm"] or ""
                }
            }

            insert_result = words_collection.insert_one(doc)
            print(f"Inserted Italian word '{doc['word']}' with _id={insert_result.inserted_id}")

    print("Italian words import complete!")

if __name__ == "__main__":
    csv_file_path = "csv/italian/italianWords.csv"
    import_italian_words(csv_file_path)
