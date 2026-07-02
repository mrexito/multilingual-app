"use client";

import { FC } from "react";

interface InlineCheckboxGroupProps {
  options: string[];
  selected: string | null;
  onChange: (newSelected: string | null) => void;
}

export const InlineCheckboxGroup: FC<InlineCheckboxGroupProps> = ({
  options,
  selected,
  onChange,
}) => {
  const handleToggle = (option: string) => {
    if (selected === option) {
      onChange(null);
    } else {
      onChange(option);
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-4">
      {options.map((option) => {
        const isChecked = selected === option;

        return (
          <label key={option} className="inline-flex items-center gap-1">
            <input
              type="checkbox"
              checked={isChecked}
              onChange={() => handleToggle(option)}
              className="rounded border-gray-300 text-primary focus:ring-primary"
            />
            <span>{option}</span>
          </label>
        );
      })}
    </div>
  );
};
