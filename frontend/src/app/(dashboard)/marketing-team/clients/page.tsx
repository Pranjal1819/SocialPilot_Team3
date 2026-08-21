"use client";

import { useState } from "react";
import Link from "next/link";
import { Search } from "lucide-react";
import { useAssignedClients } from "@/hooks/useAssignedClients";

export default function ClientsPage() {
  const [query, setQuery] = useState("");
  const { clients, loading, error } = useAssignedClients();

  const filtered = clients.filter((c) =>
    c.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div>
      <div className="relative max-w-sm">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search clients…"
          className="w-full border border-border bg-surface py-2 pl-9 pr-3 text-sm outline-none focus:border-accent-hover"
        />
      </div>

      <div className="mt-6 divide-y divide-border border border-border bg-surface">
        {loading ? (
          <p className="px-5 py-6 text-sm text-muted">Loading assigned clients…</p>
        ) : error ? (
          <p className="px-5 py-6 text-sm text-muted">{error}</p>
        ) : filtered.length === 0 ? (
          <p className="px-5 py-6 text-sm text-muted">
            {query ? `No clients match "${query}".` : "No clients assigned to you yet."}
          </p>
        ) : (
          filtered.map((client) => (
            <Link
              key={client.id}
              href={`/marketing-team/clients/${client.id}`}
              className="flex items-center justify-between px-5 py-4 hover:bg-background"
            >
              <span className="font-medium">{client.name}</span>
              <span className="text-xs text-muted">
                {client.organization || client.email}
              </span>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}