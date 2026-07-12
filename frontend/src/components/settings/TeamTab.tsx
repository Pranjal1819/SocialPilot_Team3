"use client";

import { ROLE_LABELS, Role } from "@/types/user";
import { UserPlus } from "lucide-react";

interface TeamMember {
  id: string;
  name: string;
  email: string;
  role: Role;
}

const teamMembers: TeamMember[] = [
  { id: "1", name: "Pranjal", email: "pranjal@socialpilot.com", role: "administrator" },
  { id: "2", name: "Namratha", email: "namratha@socialpilot.com", role: "content_creator" },
  { id: "3", name: "Aditi", email: "aditi@socialpilot.com", role: "marketing_team" },
  { id: "4", name: "Rohan", email: "rohan@socialpilot.com", role: "business_user" },
];

export default function TeamTab() {
  return (
    <div className="max-w-3xl rounded-2xl border border-slate-100 bg-white p-8 shadow-[0_8px_22px_-12px_rgba(15,23,42,0.1)]">
      <div className="flex items-center justify-between mb-7">
        <p className="text-base font-semibold text-slate-800">{teamMembers.length} team members</p>
        <button className="flex items-center gap-2 rounded-lg bg-[#0077B6] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#00618f] transition-colors">
          <UserPlus size={16} />
          Invite member
        </button>
      </div>

      <div className="divide-y divide-slate-100">
        {teamMembers.map((member) => (
          <div key={member.id} className="flex items-center justify-between gap-4 py-5 first:pt-0 last:pb-0">
            <div className="flex items-center gap-4 min-w-0">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[#0077B6] text-base font-semibold text-white">
                {member.name.charAt(0)}
              </div>
              <div className="min-w-0">
                <p className="text-base font-medium text-slate-900">{member.name}</p>
                <p className="text-sm text-slate-400 truncate">{member.email}</p>
              </div>
            </div>
            <span className="shrink-0 rounded-full bg-[#EAF8FC] px-3.5 py-1.5 text-sm font-medium text-[#0077B6]">
              {ROLE_LABELS[member.role]}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}