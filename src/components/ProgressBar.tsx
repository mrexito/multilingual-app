"use client";

import { IoClose } from "react-icons/io5";

type ExerciseStatus = "right" | "wrong" | "default";

export type ExerciseProgress = {
  id: string;
  status: ExerciseStatus;
};

type ProgressBarProps = {
  exercises: ExerciseProgress[];
  activeIndex: number;
  onCancel: () => void;
};

export default function ProgressBar({
  exercises,
  activeIndex,
  onCancel,
}: ProgressBarProps) {
  return (
    <div className="flex items-center gap-4">
      <IoClose
        size={32}
        className="text-xl cursor-pointer hover:text-red-500 text-start"
        onClick={onCancel}
      />
      {exercises.map((exercise, i) => {
        let bgClass = "bg-white";
        if (exercise.status === "right") bgClass = "bg-[#39BF17]";
        if (exercise.status === "wrong") bgClass = "bg-[#E20909]";

        const borderClass =
          i === activeIndex ? "border-2 border-[#31639C]" : "";

        return (
          <div
            key={exercise.id}
            className={`w-8 h-6 rounded-sm ${bgClass} ${borderClass}`}
          />
        );
      })}
    </div>
  );
}
