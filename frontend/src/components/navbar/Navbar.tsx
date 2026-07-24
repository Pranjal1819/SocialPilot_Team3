"use client";

import { Bell, ChevronDown } from "lucide-react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_LABELS } from "@/types/user";
import { ROLE_ACCENTS } from "@/constants/theme";
import FilterDropdown from "./FilterDropdown";
import GlobalSearch from "./GlobalSearch";

export default function Navbar() {
  const { name, role } = useCurrentUser();
  const initial = name.charAt(0).toUpperCase();
  const accent = ROLE_ACCENTS[role];

  return (
    <header className="flex h-[72px] items-center justify-between gap-4 border-b border-slate-200 bg-white px-4 sm:px-6 lg:px-8">
      <div className="flex max-w-3xl min-w-0 flex-1 items-center gap-3">
        <GlobalSearch />
        <FilterDropdown />
      </div>

      <div className="flex items-center gap-3 shrink-0">
        <button className="relative flex h-10 w-10 items-center justify-center rounded-lg text-slate-500 transition-all duration-150 ease-in-out hover:bg-slate-100 hover:text-slate-900">
          <Bell size={19} />
          <span className="absolute -top-1 -right-1 flex h-4 min-w-[16px] items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white ring-2 ring-white">
            2
          </span>
        </button>

        <div className="hidden h-6 w-px bg-slate-200 sm:block" />

        <button className="flex items-center gap-2.5 rounded-lg py-1.5 pl-1.5 pr-2.5 transition-colors hover:bg-slate-50">
          <div
            className="flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold text-white"
            style={{ backgroundColor: accent.solid }}
          >
            {initial}
          </div>
          <div className="hidden text-left sm:block">
            <p className="text-sm font-semibold leading-tight text-slate-900">{name}</p>
            <p className="text-xs leading-tight font-medium" style={{ color: accent.text }}>
              {ROLE_LABELS[role]}
            </p>
          </div>
          <ChevronDown size={15} className="text-slate-400" />
        </button>
      </div>
    </header>
  );
}
