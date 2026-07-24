"use client";

import { useState } from "react";
import { User, Shield, Users } from "lucide-react";
import ProfileTab from "./ProfileTab";
import AccountTab from "./AccountTab";
import TeamTab from "./TeamTab";

const tabs = [
  { key: "profile", label: "Profile", icon: User },
  { key: "account", label: "Account", icon: Shield },
  { key: "team", label: "Team", icon: Users },
] as const;

type TabKey = (typeof tabs)[number]["key"];

export default function SettingsTabs() {
  const [active, setActive] = useState<TabKey>("profile");

  return (
    <div>
      <div className="grid grid-cols-3 gap-1 rounded-2xl border border-slate-100 bg-white p-2 shadow-md">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = active === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActive(tab.key)}
              className={`flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-300 ${
                isActive
                  ? "bg-sky-50 text-[#0077B6]"
                  : "text-slate-500 hover:bg-slate-50 hover:text-slate-800"
              }`}
            >
              <Icon size={17} />
              {tab.label}
            </button>
          );
        })}
      </div>

      <div className="mt-6">{active === "profile" && <ProfileTab />}
      {active === "account" && <AccountTab />}
      {active === "team" && <TeamTab />}</div>
    </div>
  );
}
