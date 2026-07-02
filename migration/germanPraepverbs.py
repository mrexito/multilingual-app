from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import logging

logging.basicConfig(filename='migration_errors.log', level=logging.WARNING)

old_db_uri = "URI"
new_db_uri = "URI"
old_db_name = "German"
new_db_name = "multilingual-language"
old_client = MongoClient(old_db_uri)
new_client = MongoClient(new_db_uri)
old_db = old_client[old_db_name]
new_db = new_client[new_db_name]
source_collection = old_db["praepverbens"]
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

def get_subcategory_id(subcategory_name, category_id, language_id):
    category = categories_collection.find_one({"_id": category_id, "language_id": language_id})
    if not category or "subcategories" not in category:
        return None
    for subcategory in category["subcategories"]:
        if subcategory["name"] == subcategory_name:
            return subcategory["_id"]
    return None

def migrate_prepositional_verbs():
    language_id = get_language_id()
    category_id = get_category_id("Verben", language_id)
    subcategory_id = get_subcategory_id("Präpositionsverben", category_id, language_id)

    for doc in source_collection.find():
        try:
            mapped = {
                "language_id": language_id,
                "category_id": category_id,
                "subcategory_id": subcategory_id,
                "exercise_type": "fillintheblank",
                "question": doc.get("Satz", ""),
                "related_verb": doc.get("Verb", ""),
                "examples": doc.get("Beispiele", "").split("\r\n"),
                "explanation": doc.get("Erklaerung", ""),
                "correct_answer": doc.get("Loesung", ""),
                "source": doc.get("quelle", "Unknown"),
                "metadata": {
                    "date": doc.get("Datum"),
                    "tags": ["Prepositional Verbs", "Grammar"]
                }
            }
            target_collection.insert_one(mapped)
            print(f"Migrated: {mapped['question']}")
        except errors.DuplicateKeyError:
            logging.warning(f"Duplicate skipped for document _id={doc.get('_id')}")
        except Exception as exc:
            logging.error(f"Error migrating _id={doc.get('_id')}: {exc}")

try:
    migrate_prepositional_verbs()
    print("Migration completed successfully!")
except Exception as e:
    print("Fatal error during migration:", e)