"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Search, LayoutDashboard } from "lucide-react";
import { navigation } from "@/constants/navigation";
import { platforms } from "@/constants/platforms";
import { useCurrentUser } from "@/hooks/useCurrentUser";

export default function GlobalSearch() {
  const router = useRouter();
  const { role } = useCurrentUser();
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
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

  const q = query.trim().toLowerCase();

  const matchedPages = q
    ? navigation.filter((item) => item.roles.includes(role) && item.title.toLowerCase().includes(q))
    : [];

  const matchedPlatforms = q
    ? platforms.filter((p) => p.name.toLowerCase().includes(q))
    : [];

  const hasResults = matchedPages.length > 0 || matchedPlatforms.length > 0;

  const goTo = (href: string) => {
    router.push(href);
    setQuery("");
    setIsOpen(false);
  };

  return (
    <div className="relative flex-1 max-w-md" ref={ref}>
     <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-slate-50 px-3.5 py-2.5 transition-all duration-150 ease-in-out focus-within:border-slate-300 focus-within:bg-white focus-within:ring-4 focus-within:ring-slate-100">
        <Search size={16} className="text-slate-400 shrink-0" />
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search pages or platforms..."
          className="w-full bg-transparent text-sm text-slate-900 placeholder:text-slate-400 outline-none"
        />
        <kbd className="hidden sm:inline-flex shrink-0 items-center gap-0.5 rounded border border-slate-300 bg-white px-1.5 py-0.5 text-[10px] font-medium text-slate-400">
          ⌘/
        </kbd>
      </div>

      {isOpen && q && (
        <div className="absolute left-0 top-full mt-2 w-full rounded-xl border border-slate-100 bg-white p-2 shadow-[0_12px_30px_-10px_rgba(15,23,42,0.15)] z-50 max-h-80 overflow-y-auto">
          {!hasResults && (
            <p className="px-3 py-4 text-sm text-slate-400 text-center">No results for &quot;{query}&quot;</p>
          )}

          {matchedPages.length > 0 && (
            <div className="mb-1">
              <p className="px-3 pt-2 pb-1 text-xs font-semibold text-slate-400 uppercase tracking-wide">Pages</p>
              {matchedPages.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.href}
                    onClick={() => goTo(item.href)}
                    className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                  >
                    <Icon size={16} className="text-slate-400" />
                    {item.title}
                  </button>
                );
              })}
            </div>
          )}

          {matchedPlatforms.length > 0 && (
            <div>
              <p className="px-3 pt-2 pb-1 text-xs font-semibold text-slate-400 uppercase tracking-wide">
                Social Platforms
              </p>
              {matchedPlatforms.map((platform) => (
                <button
                  key={platform.name}
                  onClick={() => goTo("/social-accounts")}
                  className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  <div
                    className="flex h-6 w-6 items-center justify-center rounded-md text-white"
                    style={
                      platform.brandColor.startsWith("linear-gradient")
                        ? { backgroundImage: platform.brandColor }
                        : { backgroundColor: platform.brandColor }
                    }
                  >
                    <platform.icon size={11} />
                  </div>
                  <span>{platform.name}</span>
                  <span className="ml-auto text-xs text-slate-400 capitalize">{platform.status}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}