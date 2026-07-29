"use client";

import { useCurrentUser } from "@/hooks/useCurrentUser";

export default function DashboardHeader() {
  const { name } = useCurrentUser();

  return (
    <div className="mb-10">
      <h1 className="text-3xl font-bold tracking-tight text-slate-900">
        Welcome, {name} !
      </h1>
    </div>
  );
}