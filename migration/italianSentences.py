import csv
from pymongo import MongoClient

db_uri = "URI"
client = MongoClient(db_uri)

database = client["multilingual-language"]
words_collection = database["words"]
languages_collection = database["languages"]
sentences_collection = database["sentences"]

def get_language_id(language_name: str):
    language = languages_collection.find_one({"name": language_name})
    if not language:
        raise ValueError(f"Language '{language_name}' not found.")
    return language["_id"]

def get_word_id(word_text: str):
    word_doc = words_collection.find_one({"word": word_text})
    if not word_doc:
        return None
    return word_doc["_id"]

def import_sentences(csv_path: str):
    spanish_language_id = get_language_id("Italian")

    with open(csv_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, 
                                delimiter=';', 
                                quotechar='"', 
                                fieldnames=["Word", "Sentence"])

        for row in reader:
            sentence_text = row["Sentence"].strip()
            word_text = row["Word"].strip()

            word_id = get_word_id(word_text)
            if not word_id:
                print(f"Warning: No matching word doc found for '{word_text}'. Skipping.")
                continue
            sentence_doc = {
                "language_id": spanish_language_id,
                "word_id": word_id,
                "sentence": sentence_text
            }
            insert_result = sentences_collection.insert_one(sentence_doc)
            print(f"Inserted sentence doc with _id={insert_result.inserted_id}")

    print("Finished importing sentences!")

if __name__ == "__main__":
    import_sentences("csv/italian/italianSentences.csv")
