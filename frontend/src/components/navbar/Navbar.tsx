"use client";

import { Bell, Search } from "lucide-react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_LABELS } from "@/types/user";

export default function Navbar() {
  const { name, role } = useCurrentUser();
  const initial = name.charAt(0).toUpperCase();

  return (
    <header className="h-24 bg-[#F7FDFF] border-b border-[#CAF0F8] flex items-center justify-between px-8 gap-8">
      <div className="flex flex-1 max-w-md items-center gap-3 rounded-xl border border-[#ADE8F4]/60 bg-white px-4 py-3.5 transition-all duration-200 ease-in-out focus-within:border-[#0096C7] focus-within:ring-4 focus-within:ring-[#CAF0F8]">
        <Search size={18} className="text-slate-400 shrink-0" />
        <input
          type="text"
          placeholder="Search..."
          className="w-full bg-transparent text-sm text-slate-900 placeholder:text-slate-400 outline-none"
        />
      </div>

      <div className="flex items-center gap-5 shrink-0">
        <button className="relative flex h-11 w-11 items-center justify-center rounded-xl text-slate-500 transition-all duration-200 ease-in-out hover:bg-white hover:text-slate-900">
          <Bell size={20} />
          <span className="absolute top-2.5 right-2.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-white" />
        </button>

        <div className="flex items-center gap-3 border-l border-[#ADE8F4] pl-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#0077B6] text-sm font-semibold text-white">
            {initial}
          </div>
          <div>
            <p className="text-sm font-semibold leading-tight text-slate-900">{name}</p>
            <p className="text-xs leading-tight text-slate-400">{ROLE_LABELS[role]}</p>
          </div>
        </div>
      </div>
    </header>
  );
}