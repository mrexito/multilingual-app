/* components/exercises/Images.tsx */
"use client";

import { useState } from "react";
import { RawImageCard } from "@/lib/images";
import { Button } from "../ui/button";
import { motion, AnimatePresence } from "framer-motion";
import { FiArrowLeft, FiArrowRight } from "react-icons/fi";

type Props = { cards: RawImageCard[] };

export default function ImagesFlashcards({ cards }: Props) {
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const card = cards[idx];
  const go = (d: -1 | 1) => {
    setFlipped(false);
    setIdx((p) => (p + d + cards.length) % cards.length);
  };

  return (
    <div className="p-4 text-white mt-12 flex flex-col items-center space-y-6">
      <h2 className="text-2xl font-bold mb-2">Vegetable Flashcards</h2>

      <AnimatePresence mode="popLayout">
        <motion.div
          key={card.id + (flipped ? "-back" : "-front")}
          initial={{ opacity: 0, rotateY: flipped ? 180 : 0 }}
          animate={{ opacity: 1, rotateY: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="w-[320px] md:w-[460px] h-[320px] md:h-[380px] relative"
        >
          <div
            onClick={() => setFlipped(!flipped)}
            className="absolute inset-0 rounded-xl border-2 border-[#6A6A6A] bg-[#141F24] flex items-center justify-center cursor-pointer overflow-hidden"
          >
            {!flipped ? (
              <img
                src={card.image}
                alt="Vegetable"
                className="object-contain max-w-full max-h-full rounded-xl"
              />
            ) : (
              <div className="p-4 text-center space-y-2">
                <h3 className="text-lg font-semibold mb-2">Translations</h3>
                <ul className="space-y-1 text-sm">
                  {card.translations.map((t, i) => (
                    <li key={i}>
                      <span className="font-bold uppercase text-gray-300">
                        {mapLangLabel(t.language_id)}:
                      </span>{" "}
                      {t.translation}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </motion.div>
      </AnimatePresence>

      <div className="flex items-center space-x-4 mt-4">
        <Button onClick={() => go(-1)}><FiArrowLeft /></Button>
        <Button onClick={() => go(1)}><FiArrowRight /></Button>
      </div>
    </div>
  );
}

function mapLangLabel(id: string) {
  const map: Record<string, string> = {
    "67bed42569a3680a95974aa9": "EN",
    "67bed42569a3680a95974aaa": "ES",
    "67bed42569a3680a95974aab": "IT",
    "67bed4528f87b8e3161ad51b": "DE",
    "680b9178e6c767baf3bc3803": "FR",
  };
  return map[id] ?? id.slice(0, 5);
}
