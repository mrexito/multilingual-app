import db from "./db";

export async function getLanguages() {
  return db.languages.findMany();
}

export async function getGermanLanguage() {
  return db.languages.findFirst({
    where: {
      name: "German",
    },
  });
}

export async function getLanguageByName(language: string) {
  return db.languages.findFirst({
    where: {
      name: language,
    },
  });
}
