"use client";

import StatCard from "@/components/dashboard/StatCard";
import { useParams } from "next/navigation";
import { useAssignedClients } from "@/hooks/useAssignedClients";

export default function ClientOverview() {
  const { businessOwnerId } = useParams<{ businessOwnerId: string }>();
  const { clients } = useAssignedClients();
  const client = clients.find((item) => String(item.id) === businessOwnerId);

  if (!client) return null;

  return (
    <div className="space-y-6">
      <div className="border border-border bg-surface p-5">
        <p className="font-mono text-xs text-muted">CLIENT OVERVIEW</p>
        <p className="mt-1 font-display text-xl font-bold">{client.name}</p>
        <p className="mt-1 text-sm text-muted">
          {client.organization || client.email}
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Active Campaigns" value="—" />
        <StatCard label="Scheduled Posts" value="—" />
        <StatCard label="Published Posts" value="—" />
        <StatCard label="Engagement" value="—" hint="Avg. across published posts" />
      </div>
    </div>
  );
}