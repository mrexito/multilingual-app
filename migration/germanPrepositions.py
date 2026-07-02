from pymongo import MongoClient
from bson.objectid import ObjectId

old_db_uri = "URI"
new_db_uri = "URI"

old_db_name = "German"
new_db_name = "multilingual-language"

old_client = MongoClient(old_db_uri)
new_client = MongoClient(new_db_uri)

old_db = old_client[old_db_name]
new_db = new_client[new_db_name]

source_collection = old_db["praepositions"]
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

def migrate_prepositions_exercises():
    print(f"Starting migration from {source_collection.name} to {target_collection.name}...")

    language_id = get_language_id()
    category_id = get_category_id("Präpositionen", language_id)

    for document in source_collection.find():
        mapped_exercise = {
            "language_id": language_id,
            "category_id": category_id,
            "subcategory_id": None,
            "exercise_type": "fillintheblank",
            "question": document.get("Satz", ""),
            "correct_answer": document.get("Loesung", ""),
            "source": document.get("quelle", "Unknown"),
            "metadata": {
                "date": document.get("Datum", None),
                "tags": ["Prepositions", "Grammar"]
            }
        }
        target_collection.insert_one(mapped_exercise)
        print(f"Migrated exercise: {mapped_exercise['question']}")

    print("Migration completed successfully!")

try:
    migrate_prepositions_exercises()
except Exception as e:
    print("An error occurred during migration:", e)
