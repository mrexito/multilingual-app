from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("URI")
db = client["multilingual-language"]
languages_collection = db["languages"]
categories_collection = db["categories"]

languages = ["German", "English", "Spanish", "Italian"]

type_of_word_mapping = {
    "Adjektiv": {
        "names": {"German": "Adjektive", "English": "Adjectives", "Spanish": "Adjetivos", "Italian": "Aggettivi"},
        "type": "Vocabulary",
        "subcategories": []
    },
    "Adverb": {
        "names": {"German": "Adverbien", "English": "Adverbs", "Spanish": "Adverbios", "Italian": "Avverbi"},
        "type": "Vocabulary",
        "subcategories": []
    },
    "Nomen": {
        "names": {"German": "Nomen", "English": "Nouns", "Spanish": "Sustantivos", "Italian": "Sostantivi"},
        "type": "Vocabulary",
        "subcategories": [
            {"names": {"German": "Eigennamen", "English": "Proper Nouns", "Spanish": "Nombres Propios", "Italian": "Nomi Propri"}},
            {"names": {"German": "Gattungsnamen", "English": "Common Nouns", "Spanish": "Nombres Comunes", "Italian": "Nomi Comuni"}}
        ]
    },
    "Verben": {
        "names": {"German": "Verben", "English": "Verbs", "Spanish": "Verbos", "Italian": "Verbi"},
        "type": "Grammar",
        "subcategories": [
            {"names": {"German": "Transitive Verben", "English": "Transitive Verbs", "Spanish": "Verbos Transitivos", "Italian": "Verbi Transitivi"}},
            {"names": {"German": "Intransitive Verben", "English": "Intransitive Verbs", "Spanish": "Verbos Intransitivos", "Italian": "Verbi Intransitivi"}},
            {"names": {"German": "Reflexive Verben", "English": "Reflexive Verbs", "Spanish": "Verbos Reflexivos", "Italian": "Verbi Riflessivi"}},
            {"names": {"German": "Unpersönliche Verben", "English": "Impersonal Verbs", "Spanish": "Verbos Impersonales", "Italian": "Verbi Impersonali"}}
        ]
    },
    "Präposition": {
        "names": {"German": "Präpositionen", "English": "Prepositions", "Spanish": "Preposiciones", "Italian": "Preposizioni"},
        "type": "Grammar",
        "subcategories": []
    },
    "Konjunktion": {
        "names": {"German": "Konjunktionen", "English": "Conjunctions", "Spanish": "Conjunciones", "Italian": "Congiunzioni"},
        "type": "Grammar",
        "subcategories": []
    },
    "Artikel": {
        "names": {"German": "Artikel", "English": "Articles", "Spanish": "Artículos", "Italian": "Articoli"},
        "type": "Grammar",
        "subcategories": [
            {"names": {"German": "Bestimmte Artikel", "English": "Definite Articles", "Spanish": "Artículos Definidos", "Italian": "Articoli Determinativi"}},
            {"names": {"German": "Unbestimmte Artikel", "English": "Indefinite Articles", "Spanish": "Artículos Indefinidos", "Italian": "Articoli Indeterminativi"}}
        ]
    },
    "Pronomen": {
        "names": {"German": "Pronomen", "English": "Pronouns", "Spanish": "Pronombres", "Italian": "Pronomi"},
        "type": "Vocabulary",
        "subcategories": [
            {"names": {"German": "Personalpronomen", "English": "Personal Pronouns", "Spanish": "Pronombres Personales", "Italian": "Pronomi Personali"}},
            {"names": {"German": "Relativpronomen", "English": "Relative Pronouns", "Spanish": "Pronombres Relativos", "Italian": "Pronomi Relativi"}},
            {"names": {"German": "Demonstrativpronomen", "English": "Demonstrative Pronouns", "Spanish": "Pronombres Demostrativos", "Italian": "Pronomi Dimostrativi"}},
            {"names": {"German": "Possessivpronomen", "English": "Possessive Pronouns", "Spanish": "Pronombres Posesivos", "Italian": "Pronomi Possessivi"}}
        ]
    },
    "Partizip": {
        "names": {"German": "Partizipien", "English": "Participles", "Spanish": "Participios", "Italian": "Participi"},
        "type": "Grammar",
        "subcategories": [
            {"names": {"German": "Partizip I", "English": "Present Participle", "Spanish": "Participio Presente", "Italian": "Participio Presente"}},
            {"names": {"German": "Partizip II", "English": "Past Participle", "Spanish": "Participio Pasado", "Italian": "Participio Passato"}}
        ]
    },
    "Interjektion": {
        "names": {"German": "Interjektionen", "English": "Interjections", "Spanish": "Interjecciones", "Italian": "Interiezioni"},
        "type": "Vocabulary",
        "subcategories": []
    },
    "Numeral": {
        "names": {"German": "Numerale", "English": "Numerals", "Spanish": "Numerales", "Italian": "Numerali"},
        "type": "Vocabulary",
        "subcategories": [
            {"names": {"German": "Kardinalzahlen", "English": "Cardinal Numbers", "Spanish": "Números Cardinales", "Italian": "Numeri Cardinali"}},
            {"names": {"German": "Ordinalzahlen", "English": "Ordinal Numbers", "Spanish": "Números Ordinales", "Italian": "Numeri Ordinali"}}
        ]
    },
    "Redewendung": {
        "names": {"German": "Redewendung", "English": "Idiom", "Spanish": "Modismo", "Italian": "Idioma"},
        "type": "Vocabulary",
        "subcategories": []
    },
    "Ausdruck": {
        "names": {"German": "Ausdrücke", "English": "Expressions", "Spanish": "Expresiones", "Italian": "Espressioni"},
        "type": "Vocabulary",
        "subcategories": []
    },
    "": {
        "names": {"German": "Allgemein", "English": "General", "Spanish": "General", "Italian": "Generale"},
        "type": "General",
        "subcategories": []
    }
}

try:
    for language_name in languages:
        language = languages_collection.find_one({"name": language_name})
        if not language:
            raise Exception(f"Language '{language_name}' not found in the database.")
        language_id = language["_id"]

        for type_of_word, category_data in type_of_word_mapping.items():
            category_name = category_data["names"][language_name]

            existing_category = categories_collection.find_one({"name": category_name, "language_id": language_id})
            if existing_category:
                print(f"Category '{category_name}' already exists for '{language_name}'. Skipping.")
                continue

            subcategories = []
            for subcategory in category_data.get("subcategories", []):
                subcategory_name = subcategory["names"].get(language_name, None)
                if not subcategory_name:
                    print(f"Skipping subcategory due to missing name for '{language_name}'.")
                    continue

                subcategories.append({
                    "_id": ObjectId(),
                    "name": subcategory_name,
                    "description": f"Learn about {subcategory_name} in {language_name}"
                })

            category_document = {
                "language_id": language_id,
                "name": category_name,
                "description": f"Learn about {category_name} in {language_name}",
                "type": category_data["type"],
                "subcategories": subcategories
            }

            result = categories_collection.insert_one(category_document)
            print(f"Added category '{category_name}' for '{language_name}' with ID: {result.inserted_id}")

except Exception as e:
    print("An error occurred:", e)