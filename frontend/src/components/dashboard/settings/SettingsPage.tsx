"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ShieldCheck, SlidersHorizontal } from "lucide-react";
import SecuritySettings from "./SecuritySettings";
import PreferenceSettings from "./PreferenceSettings";

const BASE_TABS = [
  { key: "security", label: "Security", icon: ShieldCheck },
  { key: "preferences", label: "Preferences", icon: SlidersHorizontal },
] as const;

// Notification preferences live in the Notification Center itself
// (Module 7) now, not here — see components/dashboard/notifications/.
// Keeping one source of truth instead of two overlapping toggle sets.
export default function SettingsPage() {
  const [active, setActive] = useState<string>(BASE_TABS[0].key);

  return (
    <div>
      <div className="flex gap-1 border-b border-border">
        {BASE_TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActive(tab.key)}
            className="relative flex items-center gap-2 px-4 py-3 text-sm"
          >
            <tab.icon size={14} className={active === tab.key ? "text-ink" : "text-muted"} />
            <span className={active === tab.key ? "text-ink" : "text-muted"}>{tab.label}</span>
            {active === tab.key ? (
              <motion.span
                layoutId="settings-tab-underline"
                className="absolute inset-x-0 -bottom-px h-[2px] bg-accent"
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            ) : null}
          </button>
        ))}
      </div>

      <div className="mt-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={active}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {active === "security" ? <SecuritySettings /> : null}
            {active === "preferences" ? <PreferenceSettings /> : null}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
