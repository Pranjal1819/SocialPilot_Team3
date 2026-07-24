"use client";

import { LucideIcon } from "lucide-react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_ACCENTS } from "@/constants/theme";

export interface TabItem<T extends string> {
  key: T;
  label: string;
  icon: LucideIcon;
  count?: number;
}

interface Props<T extends string> {
  tabs: TabItem<T>[];
  active: T;
  onChange: (key: T) => void;
}

export default function TabBar<T extends string>({ tabs, active, onChange }: Props<T>) {
  const { role } = useCurrentUser();
  const accent = ROLE_ACCENTS[role];

  return (
    <div className="grid w-full grid-cols-2 gap-1 rounded-2xl border border-slate-100 bg-white p-2 shadow-md sm:grid-cols-4">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = active === tab.key;
        return (
          <button
            key={tab.key}
            onClick={() => onChange(tab.key)}
            className="flex min-w-0 items-center justify-center gap-2 rounded-xl px-3 py-3 text-sm font-medium transition-all duration-300 hover:bg-slate-50"
            style={
              isActive
                ? { backgroundColor: "white", color: accent.text, boxShadow: "0 1px 3px rgba(15,23,42,0.1)" }
                : { color: "#64748B" }
            }
          >
            <Icon size={15} />
            {tab.label}
            {typeof tab.count === "number" && tab.count > 0 && (
              <span
                className="flex h-4 min-w-[16px] items-center justify-center rounded-full px-1 text-[10px] font-semibold text-white"
                style={{ backgroundColor: isActive ? accent.solid : "#94A3B8" }}
              >
                {tab.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
