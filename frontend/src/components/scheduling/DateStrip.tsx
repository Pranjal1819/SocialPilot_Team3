"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_ACCENTS } from "@/constants/theme";

interface Props {
  value: string;
  onChange: (value: string) => void;
}

function toISODate(d: Date) {
  return d.toISOString().split("T")[0];
}

export default function DateStrip({ value, onChange }: Props) {
  const { role } = useCurrentUser();
  const accent = ROLE_ACCENTS[role];

  const selectedDate = new Date(value + "T00:00:00");
  const days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(selectedDate);
    d.setDate(selectedDate.getDate() - 3 + i);
    return d;
  });

  const shift = (offset: number) => {
    const d = new Date(selectedDate);
    d.setDate(d.getDate() + offset);
    onChange(toISODate(d));
  };

  return (
    <div className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white p-2.5">
      <button
        type="button"
        onClick={() => shift(-7)}
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-slate-400 hover:bg-slate-50"
      >
        <ChevronLeft size={17} />
      </button>

      {days.map((d) => {
        const iso = toISODate(d);
        const isSelected = iso === value;
        return (
          <button
            key={iso}
            type="button"
            onClick={() => onChange(iso)}
            className="flex flex-1 flex-col items-center gap-1.5 rounded-xl px-3 py-3.5 transition-all duration-150 ease-in-out"
            style={isSelected ? { backgroundColor: accent.soft } : undefined}
          >
            <span
              className="text-xs font-medium uppercase tracking-wide"
              style={{ color: isSelected ? accent.text : "#94A3B8" }}
            >
              {d.toLocaleDateString("en-US", { weekday: "short" })}
            </span>
            <span
              className="text-base font-semibold"
              style={{ color: isSelected ? accent.solid : "#334155" }}
            >
              {d.getDate()}
            </span>
          </button>
        );
      })}

      <button
        type="button"
        onClick={() => shift(7)}
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-slate-400 hover:bg-slate-50"
      >
        <ChevronRight size={17} />
      </button>
    </div>
  );
}