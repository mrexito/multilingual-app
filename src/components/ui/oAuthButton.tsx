"use client";

import { signIn } from "next-auth/react";
import { FaGithub, FaGoogle } from "react-icons/fa";
import { Button } from "./button";
import clsx from "clsx";

type OAuthButtonProps = {
  provider: "github" | "google";
  label: string;
  className?: string;
};

export default function OAuthButton({
  provider,
  label,
  className,
}: OAuthButtonProps) {
  const providerConfig = {
    github: {
      icon: <FaGithub size={24} className="text-white" />,
      bgColor: "bg-[#475467] hover:bg-[#2a313c] text-white",
    },
    google: {
      icon: <FaGoogle size={24} className="text-white" />,
      bgColor: "bg-[#475467] hover:bg-[#2a313c] text-white",
    },
  };

  return (
    <Button
      onClick={() => signIn(provider)}
      className={clsx(
        "w-full flex items-center gap-3 px-4 py-2 rounded-md justify-center",
        providerConfig[provider].bgColor,
        className
      )}
    >
      {providerConfig[provider].icon}
      <span className="font-medium">{label}</span>
    </Button>
  );
}
