"use client";

import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_LABELS } from "@/types/user";

export default function DashboardHeader() {
  const { name, role } = useCurrentUser();

  return (
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-cyan-600">Workspace overview</p>
        <h1 className="mt-1 text-4xl font-bold tracking-tight text-slate-900">Welcome back, {name}</h1>
        <p className="mt-3 text-sm leading-6 text-gray-600">
          Here&apos;s what&apos;s happening across your {ROLE_LABELS[role].toLowerCase()} workspace today.
        </p>
      </div>
    </div>
  );
}
