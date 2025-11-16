// src/lib/images.ts
import db from "./db";

export type ImageTranslation = {
  language_id: string;
  translation: string;
};

export type ImageCard = {
  id: string;
  first_image: string;
  second_image?: string | null;
  translations: ImageTranslation[];
  category?: string | null;
};

/**
 * Ruft alle Bilderkarten (ImageCards) aus der MongoDB ab.
 */
export async function getImageCards(): Promise<ImageCard[]> {
  // Prisma greift hier auf dein Modell "images" zu.
  const docs = await (db as any).images.findMany({
    select: {
      id: true,
      first_image: true,
      second_image: true,
      translations: true,
      category: true,
    },
  });

  return docs.map((d: any) => ({
    id: String(d.id),
    first_image: d.first_image,
    second_image: d.second_image ?? null,
    translations: (d.translations ?? []).map((t: any) => ({
      language_id: String(t.language_id ?? ""),
      translation: t.translation ?? "",
    })),
    category: d.category ?? null,
  }));
}
