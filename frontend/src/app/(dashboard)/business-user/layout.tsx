import type { ReactNode } from "react";
import DashboardShell from "@/components/dashboard/layout/DashboardShell";

export default function BusinessUserLayout({ children }: { children: ReactNode }) {
  return (
    <DashboardShell navKey="business-owner" basePath="/business-user" title="Business Dashboard">
      {children}
    </DashboardShell>
  );
}
