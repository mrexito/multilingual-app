"use client";

import { useState, useRef, useEffect } from "react";
import { MdKeyboardArrowDown } from "react-icons/md";

interface FilterDropdownProps {
  name?: string;
  filters: string[];
  selected: string[];
  onChange: (selectedFilters: string[]) => void;
  multi?: boolean;
}

export function FilterDropdown({
  name = "Filters",
  filters,
  selected,
  onChange,
  multi = true,
}: FilterDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleDropdown = () => setIsOpen((prev) => !prev);

  const handleToggleFilter = (filter: string) => {
    if (!multi && selected[0] === filter) {
      onChange([]);
      setIsOpen(false);
    } else if (!multi && selected[0] !== filter) {
      onChange([filter]);
      setIsOpen(false);
    } else {
      if (selected.includes(filter)) {
        onChange(selected.filter((f) => f !== filter));
      } else {
        onChange([...selected, filter]);
      }
    }
  };

  const getButtonLabel = () => {
    if (selected.length === 0) {
      return name;
    }
    if (!multi) {
      return selected[0] || name;
    }
    if (selected.length === 1) {
      return selected[0];
    }
    return `${selected.length} selected`;
  };

  return (
    <div className="relative inline-block" ref={dropdownRef}>
      <button
        type="button"
        onClick={toggleDropdown}
        className="inline-flex items-center rounded-md border border-gray-300 bg-white py-2 px-3 text-gray-700 text-sm font-medium hover:bg-gray-50 focus:outline-none"
      >
        <span className="mr-2">{getButtonLabel()}</span>
        <MdKeyboardArrowDown
          className={`h-5 w-5 transition-transform duration-200 ${
            isOpen ? "rotate-180" : "rotate-0"
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute left-0 mt-2 w-48 rounded-md bg-white shadow-lg border border-gray-100 z-10">
          <ul className="py-1 max-h-60 overflow-auto">
            {filters.map((filter) => {
              const isChecked = selected.includes(filter);

              const itemClasses = isChecked
                ? "flex items-center w-full text-left px-4 py-2 text-sm bg-gray-100 text-gray-900 font-semibold"
                : "flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900";
              return (
                <li key={filter}>
                  <button
                    type="button"
                    onClick={() => handleToggleFilter(filter)}
                    className={itemClasses}
                  >
                    {multi && (
                      <input
                        type="checkbox"
                        checked={isChecked}
                        readOnly
                        className="mr-2"
                      />
                    )}
                    {filter}
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}
