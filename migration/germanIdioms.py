from pymongo import MongoClient
import random

old_db_uri = "URI"
new_db_uri = "URI"

old_db_name = "German"
new_db_name = "multilingual-language"

old_client = MongoClient(old_db_uri)
new_client = MongoClient(new_db_uri)

old_db = old_client[old_db_name]
new_db = new_client[new_db_name]

source_collection = old_db["redewendungs"]
target_collection = new_db["exercises"]
languages_collection = new_db["languages"]
categories_collection = new_db["categories"]

def get_language_id(language_name="German"):
    language = languages_collection.find_one({"name": language_name})
    if not language:
        raise Exception(f"Language '{language_name}' not found in the database.")
    return language["_id"]

def get_category_id(category_name, language_id):
    category = categories_collection.find_one({"name": category_name, "language_id": language_id})
    if not category:
        raise Exception(f"Category '{category_name}' not found for language_id '{language_id}'.")
    return category["_id"]

def generate_options(correct_answer, all_possible_answers):
    wrong_options = random.sample([ans for ans in all_possible_answers if ans != correct_answer], 3)
    options = wrong_options + [correct_answer]
    random.shuffle(options)
    return options

def map_and_migrate():
    print(f"Starting migration from {source_collection.name} to {target_collection.name}...")

    language_id = get_language_id()
    category_id = get_category_id("Redewendung", language_id)

    all_idioms = list(source_collection.find({}, {"Redewendung": 1, "Beispiel": 1}))

    for document in source_collection.find():
        idiom = document.get("Redewendung", "")
        example = document.get("Beispiel", "")
        explanation = document.get("Erklaerung", "")
        source = document.get("Quelle", "")

        question = f"Welche Redewendung bedeutet: '{example}'?"

        correct_answer = idiom  

        options = generate_options(correct_answer, [entry["Redewendung"] for entry in all_idioms])

        mapped_document = {
            "language_id": language_id,
            "category_id": category_id,
            "exercise_type": "idioms",
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "example": example,
            "explanation": explanation,
            "source": source
        }

        target_collection.insert_one(mapped_document)
        print(f"Migrated idiom: {idiom}")

    print("Migration completed successfully!")
try:
    map_and_migrate()
except Exception as e:
    print("An error occurred during migration:", e)
