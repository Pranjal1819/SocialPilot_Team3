"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !user) {
      fetch("/login", { method: "HEAD" })
        .then((res) => {
          if (res.ok) router.push("/login");
        })
        .catch(() => {});
    }
  }, [isLoading, user, router, pathname]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F4FBFD] text-slate-400 text-sm">
        Loading...
      </div>
    );
  }

  return <DashboardLayout>{children}</DashboardLayout>;
}