import { Role } from "@/types/user";

export const COLORS = {
  primary: "#2563EB",
  secondary: "#0F766E",
  accent: "#99F6E4",

  ocean: "#0096C7",
  oceanDark: "#0077B6",
  oceanTint: "#CAF0F8",

  // Layout — warmer canvas, ink sidebar instead of flat navy-slate
  background: "#F6F7F5",
  authBackground: "#F4FBFD",
  ink: "#12181F",
  inkSoft: "#1B2330",
  sidebar: "#1E293B",
  card: "#FFFFFF",

  text: "#0F172A",
  body: "#475569",
  placeholder: "#94A3B8",

  inputBg: "#F8FAFC",
  inputBorder: "#E2E8F0",
  inputFocus: "#93C5FD",

  success: "#10B981",
  warning: "#F59E0B",
  error: "#EF4444",
} as const;

// One accent per role — reused across the sidebar rail, role badge,
// and avatar ring so the current role is visible at a glance everywhere.
export const ROLE_ACCENTS: Record<Role, { solid: string; soft: string; text: string }> = {
  content_creator: { solid: "#14B8A6", soft: "rgba(20,184,166,0.15)", text: "#0F766E" },
  marketing_team: { solid: "#F59E0B", soft: "rgba(245,158,11,0.15)", text: "#B45309" },
  business_user: { solid: "#0096C7", soft: "rgba(0,150,199,0.15)", text: "#0077B6" },
  administrator: { solid: "#8B5CF6", soft: "rgba(139,92,246,0.15)", text: "#6D28D9" },
};
