"use client";

import { useState } from "react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { ROLE_LABELS } from "@/types/user";

export default function ProfileTab() {
  const { name, role } = useCurrentUser();
  const [fullName, setFullName] = useState(name);
  const [email, setEmail] = useState("pranjal@socialpilot.com");

  return (
    <div className="rounded-2xl border border-slate-100 bg-white p-6 shadow-md transition-all duration-300 hover:shadow-xl sm:p-7">
      <div className="mb-8 flex items-center gap-4 border-b border-slate-100 pb-7">
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#0077B6] text-2xl font-semibold text-white">
          {name.charAt(0).toUpperCase()}
        </div>
        <div>
          <p className="text-lg font-semibold text-slate-900">{name}</p>
          <p className="text-sm text-slate-400">{ROLE_LABELS[role]}</p>
        </div>
      </div>

      <div className="max-w-2xl space-y-6">
        <div>
          <label className="text-sm font-medium text-slate-600">Full name</label>
          <input
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="mt-2 w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-base outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/25"
          />
        </div>
        <div>
          <label className="text-sm font-medium text-slate-600">Email address</label>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-2 w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-base outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/25"
          />
        </div>
        <div>
          <label className="text-sm font-medium text-slate-600">Role</label>
          <input
            value={ROLE_LABELS[role]}
            disabled
            className="mt-2 w-full rounded-xl border border-gray-300 bg-slate-100 px-4 py-3 text-base text-slate-500 outline-none"
          />
          <p className="mt-2 text-sm text-slate-400">Contact an administrator to change your role.</p>
        </div>
      </div>

      <button className="mt-8 h-11 rounded-xl bg-gradient-to-br from-[#0096C7] to-[#0077B6] px-6 text-sm font-semibold text-white shadow-[0_10px_25px_-8px_rgba(0,119,182,0.4)] transition-all duration-200 hover:-translate-y-0.5">
        Save changes
      </button>
    </div>
  );
}
