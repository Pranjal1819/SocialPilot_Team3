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
      <div className="flex gap-6 mb-8 border-b border-slate-100 pb-0">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = active === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActive(tab.key)}
              className={`flex items-center gap-2 px-2 py-4 text-sm font-medium border-b-2 transition-colors ${
                isActive
                  ? "border-[#0077B6] text-[#0077B6]"
                  : "border-transparent text-slate-500 hover:text-slate-800"
              }`}
            >
              <Icon size={17} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {active === "profile" && <ProfileTab />}
      {active === "account" && <AccountTab />}
      {active === "team" && <TeamTab />}
    </div>
  );
}