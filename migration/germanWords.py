from pymongo import MongoClient

old_db_uri = "URI"
new_db_uri = "URI"

old_db_name = "German"
new_db_name = "multilingual-language"

old_client = MongoClient(old_db_uri)
new_client = MongoClient(new_db_uri)

old_db = old_client[old_db_name]
new_db = new_client[new_db_name]

source_collection = old_db["deutschs"]
target_collection = new_db["words"]
languages_collection = new_db["languages"]
categories_collection = new_db["categories"]

type_of_word_mapping = {
    "Adjektiv": {"category": "Adjektive", "subcategory": None},
    "Adverb": {"category": "Adverbien", "subcategory": None},
    "Ausdruck": {"category": "Ausdrücke", "subcategory": None},
    "Intransitives Verb": {"category": "Verben", "subcategory": "Intransitive Verben"},
    "Konjunktion": {"category": "Konjunktionen", "subcategory": None},
    "Nomen": {"category": "Nomen", "subcategory": None},
    "Partizip": {"category": "Partizipien", "subcategory": None},
    "Präposition": {"category": "Präpositionen", "subcategory": None},
    "Reflexives Verb": {"category": "Verben", "subcategory": "Reflexive Verben"},
    "Transitives Verb": {"category": "Verben", "subcategory": "Transitive Verben"},
    "Unpersönliches Verb": {"category": "Verben", "subcategory": "Unpersönliche Verben"},
    "": {"category": "Allgemein", "subcategory": None},
}

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

def get_subcategory_id(subcategory_name, language_id, category_id):
    category = categories_collection.find_one({"_id": category_id, "language_id": language_id})
    if not category or "subcategories" not in category:
        return None
    for subcategory in category["subcategories"]:
        if subcategory["name"] == subcategory_name:
            return subcategory["_id"]
    return None

def map_and_migrate():
    print(f"Starting migration from {source_collection.name} to {target_collection.name}...")

    language_id = get_language_id()

    for document in source_collection.find():
        specific_type = document.get("TypeOfWord", [{}])[0].get("TypeOfWord", "")
        mapping = type_of_word_mapping.get(specific_type, {"category": "Allgemein", "subcategory": None})
        category_name = mapping["category"]
        subcategory_name = mapping["subcategory"]

        try:
            category_id = get_category_id(category_name, language_id)

            subcategory_id = get_subcategory_id(subcategory_name, language_id, category_id) if subcategory_name else None

            mapped_document = {
                "language_id": language_id,
                "category_id": category_id,
                "subcategory_id": subcategory_id,
                "word": document.get("Word", ""),
                "type": specific_type,
                "translations": [
                    {"language": "French", "word": item.get("Transl_F", "")}
                    for item in document.get("TransL_F", [])
                ],
                "examples": [
                    item.get("Sentence_D", "")
                    for item in document.get("Article", [])
                ],
                "additional_info": {
                    "phonetics": document.get("Phonetics", ""),
                    "root": document.get("Root", ""),
                    "prefix": document.get("Prefix", ""),
                    "structure": document.get("Structure", ""),
                    "definition": document.get("Definition", ""),
                }
            }
            target_collection.insert_one(mapped_document)
            print(f"Migrated word: {mapped_document['word']}")

        except Exception as e:
            print(f"Error migrating word '{document.get('Word', '')}': {e}")

    print("Migration completed successfully!")

try:
    map_and_migrate()
except Exception as e:
    print("An error occurred during migration:", e)
