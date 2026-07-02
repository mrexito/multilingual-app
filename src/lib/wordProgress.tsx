import db from "@/lib/db";

export type CardStatus = 0 | 1 | 2;

export async function getProgressMap(
  userId: string,
  languageId?: string
): Promise<Record<string, CardStatus>> {
  const rows = await db.wordProgress.findMany({
    where: {
      user_id: userId,
      ...(languageId ? { language_id: languageId } : {}),
    },
  });
  return Object.fromEntries(
    rows.map((r) => [r.word_id, r.status])
  ) as unknown as Record<string, CardStatus>;
}

/** set an *exact* status (0 | 1 | 2) */
export async function setProgress(
  userId: string,
  languageId: string,
  wordId: string,
  status: CardStatus
) {
  await db.wordProgress.upsert({
    where: { user_id_word_id: { user_id: userId, word_id: wordId } },
    create: {
      user_id: userId,
      word_id: wordId,
      language_id: languageId,
      status,
      updated_at: new Date(),
    },
    update: { status },
  });
  return status;
}

export async function resetProgressForLanguage(
  userId: string,
  languageId: string
) {
  await db.wordProgress.deleteMany({
    where: { user_id: userId, language_id: languageId },
  });
}
