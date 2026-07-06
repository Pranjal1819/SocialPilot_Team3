"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LogOut } from "lucide-react";
import { navigation } from "@/constants/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-72 min-h-screen bg-slate-800 text-slate-300 flex flex-col">
      <div className="h-24 flex items-center px-7 border-b border-white/10">
        <h1 className="text-2xl font-bold tracking-tight text-white">
          Social<span className="text-teal-300">Pilot</span>
        </h1>
      </div>

      <nav className="flex-1 px-5 py-10">
        <ul className="space-y-4">
          {navigation.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <li key={item.title}>
                <Link
                  href={item.href}
                  className={`group relative flex items-center gap-4 rounded-xl px-4 py-4 text-base font-medium transition-all duration-200 ease-in-out ${
                    isActive ? "bg-white/10 text-white" : "text-slate-400 hover:bg-white/5 hover:text-slate-100"
                  }`}
                >
                  {isActive && (
                    <span className="absolute left-0 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-teal-300" />
                  )}
                  <Icon size={22} className={isActive ? "text-teal-300" : "text-slate-500 group-hover:text-slate-300"} />
                  <span>{item.title}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="p-5 border-t border-white/10">
        <button className="flex w-full items-center gap-4 rounded-xl px-4 py-4 text-base font-medium text-slate-400 transition-all duration-200 ease-in-out hover:bg-red-500/10 hover:text-red-400">
          <LogOut size={22} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}