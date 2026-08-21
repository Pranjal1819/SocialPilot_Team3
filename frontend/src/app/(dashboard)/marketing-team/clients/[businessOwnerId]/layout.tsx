"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, RefreshCw } from "lucide-react";
import ClientWorkspaceShell from "@/components/dashboard/layout/ClientWorkspaceShell";
import { useAssignedClients } from "@/hooks/useAssignedClients";

export default function ClientWorkspaceLayout({
  children,
  
}: {
  children: ReactNode;
}) {
  const { businessOwnerId } = useParams<{ businessOwnerId: string }>();
  const { clients, loading, error } = useAssignedClients();
  const client = clients.find((item) => String(item.id) === businessOwnerId);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-muted">
        <RefreshCw size={16} className="mr-2 animate-spin" /> Loading client workspace...
      </div>
    );
  }

  if (error || !client) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-muted">
        {error || "This client is not assigned to your team."}
      </div>
    );
  }

  return (
    <ClientWorkspaceShell
      basePath={`/marketing-team/clients/${businessOwnerId}`}
      title={`${client.name} Workspace`}
    >
      <div className="border-b border-border -mx-6 -mt-6">
        <Link
          href="/marketing-team/clients"
          className="flex items-center gap-2 px-6 py-2 text-xs text-muted hover:text-ink"
        >
          <ArrowLeft size={12} />
          All clients
        </Link>
      </div>
      {children}
    </ClientWorkspaceShell>
  );
}