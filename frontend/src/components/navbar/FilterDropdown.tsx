"use client";

import { useState, useRef, useEffect } from "react";
import { SlidersHorizontal, ChevronDown } from "lucide-react";

const filterGroups = [
  {
    label: "Status",
    options: ["Connected", "Not connected", "Token expired"],
  },
  {
    label: "Platform",
    options: ["Facebook", "Instagram", "LinkedIn", "X (Twitter)", "YouTube", "Pinterest"],
  },
];

export default function FilterDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleFilter = (option: string) => {
    setActiveFilters((prev) =>
      prev.includes(option) ? prev.filter((f) => f !== option) : [...prev, option]
    );
  };

  const clearFilters = () => setActiveFilters([]);

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setIsOpen((v) => !v)}
        className={`flex items-center gap-2 rounded-xl border px-3.5 py-2.5 text-sm font-medium transition-all duration-200 ease-in-out ${
          activeFilters.length > 0
            ? "border-blue-200 bg-blue-50 text-blue-700"
            : "border-slate-200 bg-slate-50 text-slate-600 hover:bg-white hover:border-blue-200"
        }`}
      >
        <SlidersHorizontal size={15} className={activeFilters.length > 0 ? "text-blue-600" : "text-slate-400"} />
        <span className="hidden lg:inline">Filters</span>
        {activeFilters.length > 0 && (
          <span className="flex h-5 w-5 items-center justify-center rounded-full bg-blue-600 text-[10px] font-bold text-white">
            {activeFilters.length}
          </span>
        )}
        <ChevronDown size={14} className={`text-slate-400 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-64 rounded-xl border border-slate-100 bg-white p-4 shadow-[0_12px_30px_-10px_rgba(15,23,42,0.15)] z-50">
          {filterGroups.map((group) => (
            <div key={group.label} className="mb-4 last:mb-0">
              <p className="mb-2 text-xs font-semibold text-slate-400 uppercase tracking-wide">
                {group.label}
              </p>
              <div className="space-y-1">
                {group.options.map((option) => (
                  <label
                    key={option}
                    className="flex items-center gap-2.5 rounded-lg px-2 py-1.5 text-sm text-slate-700 hover:bg-slate-50 cursor-pointer transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={activeFilters.includes(option)}
                      onChange={() => toggleFilter(option)}
                      className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    />
                    {option}
                  </label>
                ))}
              </div>
            </div>
          ))}

          {activeFilters.length > 0 && (
            <button
              onClick={clearFilters}
              className="mt-2 w-full rounded-lg border border-slate-200 py-2 text-xs font-medium text-slate-500 hover:bg-slate-50 transition-colors"
            >
              Clear all filters
            </button>
          )}
        </div>
      )}
    </div>
  );
}