import csv
from pymongo import MongoClient
from bson.objectid import ObjectId

db_uri = "URI"
client = MongoClient(db_uri)

database = client["multilingual-language"]
words_collection = database["words"]
languages_collection = database["languages"]
categories_collection = database["categories"]

def get_language_id(language_name: str):
    language = languages_collection.find_one({"name": language_name})
    if not language:
        raise ValueError(f"Language '{language_name}' not found.")
    return language["_id"]

def get_category_id(category_name: str, language_id: ObjectId):
    category = categories_collection.find_one({
        "name": category_name,
        "language_id": language_id
    })
    if not category:
        raise ValueError(f"Category '{category_name}' not found for language_id={language_id}.")
    return category["_id"]

def migrate_words_from_csv(csv_path: str):
    english_language_id = get_language_id("English")
    english_adjective_category_id = get_category_id("Adjectives", english_language_id)

    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(
            csvfile,
            delimiter=';', 
            quotechar='"',
            fieldnames=[
                "Word",
                "Phonetics",
                "DateEntryWord",
                "Definition",
                "RandomNumber",
                "CounterWords",
                "CumulWord",
                "Transl_F",
                "TypeOfWord",
                "Sentence",
                "DateSource",
                "TitleOfArticle",
                "Content",
                "Source"
            ]
        )

        for row in reader:
            word_doc = {
                "language_id": english_language_id,
                "category_id": english_adjective_category_id,
                "word": row["Word"].strip() if row["Word"] else "",
                "type": "Adjective",
                "examples": [row["Sentence"]] if row["Sentence"] else [],
                "additional_info": {
                    "phonetics": row["Phonetics"],
                    "date_entry_word": row["DateEntryWord"],
                    "definition": row["Definition"],
                    "random_number": row["RandomNumber"],
                    "counter_words": row["CounterWords"],
                    "cumul_word": row["CumulWord"],
                    "date_source": row["DateSource"],
                    "title_of_article": row["TitleOfArticle"],
                    "content": row["Content"],
                    "source": row["Source"]
                }
            }

            insert_result = words_collection.insert_one(word_doc)
            print(f"Inserted _id={insert_result.inserted_id} word='{word_doc['word']}'")

    print("CSV migration completed!")

if __name__ == "__main__":
    csv_file_path = "csv/english/englishWords.csv"
    migrate_words_from_csv(csv_file_path)
