"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, Moon, Sun, Contrast } from "lucide-react";
import { useProfileStore } from "@/store/useProfileStore";
import { TIMEZONES } from "@/lib/content";

const LANGUAGES = ["English"];

export default function PreferenceSettings() {
  const { timezone, language, updatePreferences } = useProfileStore();
  const [localTz, setLocalTz] = useState(timezone);
  const [localLang, setLocalLang] = useState(language);
  const [saved, setSaved] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark" | "contrast">("light");

  useEffect(() => {
    const stored = window.localStorage.getItem("socialpilot-theme") as "light" | "dark" | "contrast" | null;
    const initial = stored ?? "light";
    document.documentElement.dataset.theme = initial;
    setTheme(initial);
  }, []);

  function changeTheme(nextTheme: "light" | "dark" | "contrast") {
    setTheme(nextTheme);
    document.documentElement.dataset.theme = nextTheme;
    window.localStorage.setItem("socialpilot-theme", nextTheme);
  }

  function handleSave() {
    updatePreferences({ timezone: localTz, language: localLang });
    setSaved(true);
    setTimeout(() => setSaved(false), 2200);
  }

  return (
    <div className="border border-border bg-surface p-5">
      <div className="grid max-w-sm gap-4">
        <div>
          <label className="mb-1.5 block text-sm font-medium">Theme</label>
          <div className="flex gap-2">
            {([['light', Sun], ['dark', Moon], ['contrast', Contrast]] as const).map(([value, Icon]) => (
              <button key={value} type="button" onClick={() => changeTheme(value)} className={`flex items-center gap-2 border px-3 py-2 text-sm ${theme === value ? "border-ink bg-ink text-background" : "border-border bg-background"}`}>
                <Icon size={14} /> {value[0].toUpperCase() + value.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="mb-1.5 block text-sm font-medium">Default timezone</label>
          <select
            value={localTz}
            onChange={(e) => setLocalTz(e.target.value)}
            className="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none"
          >
            {TIMEZONES.map((tz) => (
              <option key={tz} value={tz}>
                {tz}
              </option>
            ))}
          </select>
          <p className="mt-1 text-xs text-muted">Used as the default when scheduling a new post.</p>
        </div>

        <div>
          <label className="mb-1.5 block text-sm font-medium">Language</label>
          <select
            value={localLang}
            onChange={(e) => setLocalLang(e.target.value)}
            className="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none"
          >
            {LANGUAGES.map((l) => (
              <option key={l} value={l}>
                {l}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="mt-5 flex items-center gap-4">
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={handleSave}
          className="bg-accent px-5 py-2.5 text-sm font-medium text-ink hover:bg-accent-hover"
        >
          Save preferences
        </motion.button>
        <AnimatePresence>
          {saved ? (
            <motion.span
              initial={{ opacity: 0, x: -6 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-1.5 text-sm text-success"
            >
              <CheckCircle2 size={15} /> Saved
            </motion.span>
          ) : null}
        </AnimatePresence>
      </div>
    </div>
  );
}
