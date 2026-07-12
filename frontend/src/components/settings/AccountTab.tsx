"use client";

import { useState } from "react";

function Toggle({ checked, onChange }: { checked: boolean; onChange: () => void }) {
  return (
    <button
      onClick={onChange}
      className={`flex h-7 w-12 shrink-0 items-center rounded-full px-0.5 transition-colors duration-200 ${
        checked ? "bg-[#0077B6] justify-end" : "bg-slate-200 justify-start"
      }`}
    >
      <span className="h-6 w-6 rounded-full bg-white shadow" />
    </button>
  );
}

export default function AccountTab() {
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [pushAlerts, setPushAlerts] = useState(false);
  const [twoFactor, setTwoFactor] = useState(false);

  const rows = [
    { label: "Email notifications", desc: "Get updates about your posts and campaigns", value: emailAlerts, onChange: () => setEmailAlerts((v) => !v) },
    { label: "Push notifications", desc: "Receive alerts on your device", value: pushAlerts, onChange: () => setPushAlerts((v) => !v) },
    { label: "Two-factor authentication", desc: "Add an extra layer of security to your account", value: twoFactor, onChange: () => setTwoFactor((v) => !v) },
  ];

  return (
    <div className="max-w-3xl rounded-2xl border border-slate-100 bg-white p-8 shadow-[0_8px_22px_-12px_rgba(15,23,42,0.1)] divide-y divide-slate-100">
      {rows.map((row) => (
        <div key={row.label} className="flex items-center justify-between gap-6 py-5 first:pt-0 last:pb-0">
          <div className="min-w-0">
            <p className="text-base font-medium text-slate-900">{row.label}</p>
            <p className="text-sm text-slate-400 mt-1">{row.desc}</p>
          </div>
          <Toggle checked={row.value} onChange={row.onChange} />
        </div>
      ))}

      <div className="pt-6">
        <button className="rounded-lg border border-red-200 px-5 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50 transition-colors">
          Delete account
        </button>
      </div>
    </div>
  );
}