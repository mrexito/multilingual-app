"use client";

import Link from "next/link";

type ExerciseCardProps = {
  name: string;
  href: string;
  description: string;
};

export default function ExerciseCard({
  name,
  description,
  href,
}: ExerciseCardProps) {
  return (
    <Link href={href} className="block">
      <div className="flex flex-col justify-center rounded-lg border-2 border-[#6A6A6A] p-4 hover:bg-gray-800 cursor-pointer">
        <p className="mb-2 text-lg font-semibold">{name}</p>
        <p className="text-sm mb-4">{description}</p>
      </div>
    </Link>
  );
}
