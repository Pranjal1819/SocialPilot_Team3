"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, UserPlus } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { EmptyState } from "@/components/ui/empty-state";
import { getManagedUsers, inviteMember, ManagedUser } from "@/lib/userManagementService";
import { ROLE_LABELS, Role } from "@/types/user";

const roles: Role[] = ["administrator", "marketing_team", "business_user", "content_creator"];

export function UserManagementPanel() {
  const [members, setMembers] = useState<ManagedUser[]>([]);
  const [query, setQuery] = useState("");
  const [showInvite, setShowInvite] = useState(false);
  const [invite, setInvite] = useState({ name: "", email: "", role: "content_creator" as Role, organization: "SocialPilot" });

  useEffect(() => { getManagedUsers().then(setMembers); }, []);
  const filtered = useMemo(() => members.filter((member) => `${member.name} ${member.email} ${ROLE_LABELS[member.role]}`.toLowerCase().includes(query.toLowerCase())), [members, query]);
  const submitInvite = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!invite.name || !invite.email) return;
    const member = await inviteMember(invite);
    setMembers((current) => [...current, member]);
    setInvite({ name: "", email: "", role: "content_creator", organization: "SocialPilot" });
    setShowInvite(false);
  };

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1"><Search className="absolute left-3.5 top-3.5 text-slate-400" size={16} /><Input value={query} onChange={(event) => setQuery(event.target.value)} className="pl-10" placeholder="Search members by name, email, or role" /></div>
        <Button onClick={() => setShowInvite((value) => !value)}><UserPlus /> Invite member</Button>
      </div>

      {showInvite && (
        <form onSubmit={submitInvite} className="grid gap-3 rounded-2xl border border-sky-100 bg-sky-50/50 p-4 sm:grid-cols-2 sm:p-5">
          <Input required value={invite.name} onChange={(event) => setInvite({ ...invite, name: event.target.value })} placeholder="Full name" />
          <Input required type="email" value={invite.email} onChange={(event) => setInvite({ ...invite, email: event.target.value })} placeholder="Email address" />
          <select value={invite.role} onChange={(event) => setInvite({ ...invite, role: event.target.value as Role })} className="h-11 rounded-xl border border-slate-200 bg-white px-3.5 text-sm outline-none focus:border-sky-400 focus:ring-4 focus:ring-sky-50">
            {roles.map((role) => <option key={role} value={role}>{ROLE_LABELS[role]}</option>)}
          </select>
          <div className="flex gap-3"><Button type="button" variant="outline" className="flex-1" onClick={() => setShowInvite(false)}>Cancel</Button><Button type="submit" className="flex-1">Send invite</Button></div>
        </form>
      )}

      {filtered.length === 0 ? <EmptyState title="No members found" description="Try a different search or invite a teammate to this workspace." /> : (
        <div className="grid gap-3 md:grid-cols-2">
          {filtered.map((member) => <article key={member.id} className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm transition hover:shadow-md">
            <div className="flex items-start justify-between gap-3"><div className="flex min-w-0 items-center gap-3"><div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-sky-700 font-semibold text-white">{member.name.charAt(0)}</div><div className="min-w-0"><h2 className="truncate text-sm font-semibold text-slate-900">{member.name}</h2><p className="truncate text-sm text-slate-500">{member.email}</p></div></div><Badge variant={member.status === "active" ? "secondary" : "outline"}>{member.status}</Badge></div>
            <div className="mt-4 flex flex-wrap gap-2"><Badge className="bg-sky-50 text-sky-700">{ROLE_LABELS[member.role]}</Badge><span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500">{member.organization}</span>{member.assignedClients > 0 && <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500">{member.assignedClients} assigned clients</span>}</div>
          </article>)}
        </div>
      )}
    </div>
  );
}
