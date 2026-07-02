import csv
from pymongo import MongoClient

db_uri = "URI"
client = MongoClient(db_uri)

database = client["multilingual-language"]
words_collection = database["words"]
languages_collection = database["languages"]

def get_language_id(language_name: str):
    """Retrieve the _id from the languages collection by name."""
    language_doc = languages_collection.find_one({"name": language_name})
    if not language_doc:
        raise ValueError(f"Language '{language_name}' not found.")
    return language_doc["_id"]

def import_spanish_words(csv_path: str):
    spanish_language_id = get_language_id("Spanish")
    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(
            csvfile,
            delimiter=';',
            quotechar='"',
            fieldnames=[
                "ID_Word", "Word", "Definition", "Structure",
                "DateEntryWord", "Var1", "RandomNumber",
                "CounterWords", "CumulWord", "Phonetics"
            ]
        )

        for row in reader:
            doc = {
                "language_id": spanish_language_id,
                "word": row["Word"] or "",
                "definition": row["Definition"] or "",
                "structure": row["Structure"] or "",
                "date_entry_word": row["DateEntryWord"] or "",
                "var1": row["Var1"] or "",
                "random_number": row["RandomNumber"] or "",
                "counter_words": row["CounterWords"] or "",
                "cumul_word": row["CumulWord"] or "",
                "phonetics": row["Phonetics"] or ""
            }
            insert_result = words_collection.insert_one(doc)
            print(f"Inserted _id={insert_result.inserted_id} word='{doc['word']}'")

    print("Finished importing Spanish words!")

if __name__ == "__main__":
    csv_file_path = "csv/spanish/spanishWords.csv"

    import_spanish_words(csv_file_path)
