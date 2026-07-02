// components/CustomInput.tsx
import React from "react";

interface ExerciseInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  onKeyDown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
  disabled?: boolean;
}

const ExerciseInput: React.FC<ExerciseInputProps> = ({
  value,
  onChange,
  placeholder = " ",
  onKeyDown,
  disabled = false,
}) => {
  return (
    <div className="relative w-full mt-16">
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="block w-full bg-transparent border-0 border-t-2 border-b-2
                   border-[#6A6A6A] px-2 py-4
                   focus:border-blue-500 focus:outline-none
                   placeholder-transparent"
        placeholder={placeholder}
        onKeyDown={onKeyDown}
        disabled={disabled}
        id="customInput"
      />
    </div>
  );
};

export default ExerciseInput;
