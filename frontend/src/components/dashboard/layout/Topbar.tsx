"use client";

import { usePathname } from "next/navigation";
import { NAV_SECTIONS, type NavKey } from "@/lib/navigation";

export default function Topbar({
  navKey,
  basePath,
  fallbackTitle,
}: {
  navKey: NavKey;
  basePath: string;
  fallbackTitle: string;
}) {
  const pathname = usePathname();

  // Match the deepest nav item whose href prefixes the current path, so a
  // sub-route like /posts/new still reads as "My Posts" rather than
  // falling back to the role-level title on every single page.
  const items = NAV_SECTIONS[navKey];
  const match = items
    .filter((item) => item.href !== "" && pathname.startsWith(`${basePath}${item.href}`))
    .sort((a, b) => b.href.length - a.href.length)[0];
  const isRoot = pathname === basePath;
  const title = isRoot ? fallbackTitle : match?.label ?? fallbackTitle;

  return (
    <header className="flex h-16 items-center border-b border-border px-6">
      <h1 className="font-display text-lg font-bold">{title}</h1>
    </header>
  );
}