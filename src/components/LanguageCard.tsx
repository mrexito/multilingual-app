"use client";

import Link from "next/link";

type LanguageCardProps = {
  name: string;
  href: string;
  icon: React.ReactNode;
};

export default function LanguageCard({ name, icon, href }: LanguageCardProps) {
  return (
    <Link href={href} className="block">
      <div className="flex flex-col items-center justify-center rounded-lg border-2 border-[#6A6A6A] p-4 hover:bg-gray-800 cursor-pointer">
        <p className="mb-2 text-lg font-semibold">{name}</p>
        {icon}
      </div>
    </Link>
  );
}
