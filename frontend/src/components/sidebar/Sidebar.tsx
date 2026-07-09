"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LogOut } from "lucide-react";
import { navigation, secondaryNavigation, NavItem } from "@/constants/navigation";
import { useCurrentUser } from "@/hooks/useCurrentUser";

function NavLink({ item, isActive }: { item: NavItem; isActive: boolean }) {
  const Icon = item.icon;

  return (
    <Link
      href={item.href}
      className={`group relative flex items-center gap-4 rounded-xl border px-4 py-3.5 text-[15px] font-medium transition-all duration-200 ease-in-out ${
        isActive
          ? "border-teal-300/30 bg-white/10 text-white"
          : "border-transparent text-slate-400 hover:border-white/10 hover:bg-white/5 hover:text-slate-100"
      }`}
    >
      {isActive && (
        <span className="absolute left-0 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-teal-300" />
      )}
      <Icon
        size={20}
        className={isActive ? "text-teal-300" : "text-slate-500 group-hover:text-slate-300"}
      />
      <span>{item.title}</span>
    </Link>
  );
}

export default function Sidebar() {
  const pathname = usePathname();
  const { role } = useCurrentUser();

  const visiblePrimary = navigation.filter((item) => item.roles.includes(role));
  const visibleSecondary = secondaryNavigation.filter((item) => item.roles.includes(role));

  return (
    <aside className="w-72 min-h-screen bg-slate-800 text-slate-300 flex flex-col">
      {/* Logo */}
      <div className="h-24 flex items-center px-7 border-b border-white/10">
        <h1 className="text-2xl font-bold tracking-tight text-white">
          Social<span className="text-teal-200">Pilot</span>
        </h1>
      </div>

      {/* Primary Navigation */}
      <nav className="flex-1 px-5 py-8">
        <ul className="space-y-3">
          {visiblePrimary.map((item) => (
            <li key={item.title}>
              <NavLink item={item} isActive={pathname === item.href} />
            </li>
          ))}
        </ul>
      </nav>

      {/* Bottom Section: Help & Support, Settings, Logout */}
      <div className="px-5 pb-6 pt-4 border-t border-white/10 space-y-3">
        {visibleSecondary.map((item) => (
          <NavLink key={item.title} item={item} isActive={pathname === item.href} />
        ))}

        <button className="flex w-full items-center gap-4 rounded-xl border border-transparent px-4 py-3.5 text-[15px] font-medium text-slate-400 transition-all duration-200 ease-in-out hover:border-red-500/20 hover:bg-red-500/10 hover:text-red-400">
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}