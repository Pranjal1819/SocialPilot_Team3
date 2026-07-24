"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LogOut, ChevronRight } from "lucide-react";
import { navigation, secondaryNavigation, NavItem } from "@/constants/navigation";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_ACCENTS, COLORS } from "@/constants/theme";
import { ROLE_LABELS } from "@/types/user";

function NavLink({ item, isActive, accent }: { item: NavItem; isActive: boolean; accent: string }) {
  const Icon = item.icon;

  return (
    <Link
      href={item.href}
      className={`group relative flex items-center justify-center gap-3 rounded-xl px-3 py-2.5 text-[14px] font-medium transition-all duration-300 ease-out sm:justify-start sm:px-3.5 ${
        isActive
          ? "bg-white/[0.08] text-white"
          : "text-slate-400 hover:bg-white/[0.04] hover:text-slate-100"
      }`}
    >
      {isActive && (
        <span
          className="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-r-full"
          style={{ backgroundColor: accent }}
        />
      )}
      <Icon
        size={17}
        style={isActive ? { color: accent } : undefined}
        className={!isActive ? "text-slate-500 group-hover:text-slate-300" : ""}
      />
      <span className="hidden sm:inline">{item.title}</span>
      {isActive && <ChevronRight size={14} className="ml-auto hidden text-slate-500 sm:block" />}
    </Link>
  );
}

export default function Sidebar() {
  const pathname = usePathname();
  const { role } = useCurrentUser();
  const accent = ROLE_ACCENTS[role];

  const visiblePrimary = navigation.filter((item) => item.roles.includes(role));
  const visibleSecondary = secondaryNavigation.filter((item) => item.roles.includes(role));

  return (
    <aside className="sticky top-0 flex h-screen w-[72px] shrink-0 flex-col border-r border-white/[0.06] sm:w-64" style={{ backgroundColor: COLORS.ink }}>
      {/* Logo + role pill */}
      <div className="px-3 pt-7 pb-6 text-center sm:px-6 sm:text-left">
        <h1 className="text-xl font-bold tracking-tight text-white">
          <span className="sm:hidden">S</span><span className="hidden sm:inline">Social<span style={{ color: accent.solid }}>Pilot</span></span>
        </h1>
        <span
          className="mt-3 hidden items-center gap-1.5 rounded-full px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider sm:inline-flex"
          style={{ backgroundColor: accent.soft, color: accent.solid }}
        >
          <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: accent.solid }} />
          {ROLE_LABELS[role]}
        </span>
      </div>

      <div className="mx-3 h-px bg-white/[0.08] sm:mx-6" />

      {/* Primary Navigation */}
      <nav className="flex-1 px-2 py-6 sm:px-3">
        <p className="hidden px-3.5 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500 sm:block">
          Menu
        </p>
        <ul className="space-y-1">
          {visiblePrimary.map((item) => (
            <li key={item.title}>
              <NavLink item={item} isActive={pathname === item.href} accent={accent.solid} />
            </li>
          ))}
        </ul>
      </nav>

      {/* Bottom Section */}
      <div className="space-y-1 border-t border-white/[0.08] px-2 pb-6 pt-4 sm:px-3">
        {visibleSecondary.map((item) => (
          <NavLink key={item.title} item={item} isActive={pathname === item.href} accent={accent.solid} />
        ))}

        <button className="flex w-full items-center justify-center gap-3 rounded-xl px-3 py-2.5 text-[14px] font-medium text-slate-400 transition-all duration-300 hover:bg-red-500/10 hover:text-red-400 sm:justify-start sm:px-3.5">
          <LogOut size={17} />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </aside>
  );
}
