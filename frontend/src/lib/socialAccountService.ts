import { ConnectionStatus, platforms } from "@/constants/platforms";

export interface SocialAccount {
  name: string;
  brandColor: string;
  icon: (typeof platforms)[number]["icon"];
  status: ConnectionStatus;
  lastSync: string | null;
  permissions: string[];
  tokenStatus: "valid" | "expired" | "needs_refresh" | "not_connected";
}

let accounts: SocialAccount[] = platforms.map((platform, index) => ({
  ...platform,
  lastSync: platform.status === "connected" ? `${index + 1}h ago` : null,
  permissions: platform.status === "connected" ? ["Publish", "Read insights"] : [],
  tokenStatus: platform.status === "error" ? "expired" : platform.status === "connected" ? "valid" : "not_connected",
}));

const delay = () => new Promise((resolve) => setTimeout(resolve, 180));
const update = (name: string, patch: Partial<SocialAccount>) => {
  accounts = accounts.map((account) => (account.name === name ? { ...account, ...patch } : account));
  return accounts.find((account) => account.name === name)!;
};

export async function getSocialAccounts(): Promise<SocialAccount[]> { await delay(); return [...accounts]; }
export async function connectPlatform(name: string) { await delay(); return update(name, { status: "connected", tokenStatus: "valid", lastSync: "Just now", permissions: ["Publish", "Read insights"] }); }
export async function disconnectPlatform(name: string) { await delay(); return update(name, { status: "disconnected", tokenStatus: "not_connected", lastSync: null, permissions: [] }); }
export async function syncPlatform(name: string) { await delay(); return update(name, { lastSync: "Just now" }); }
export async function refreshToken(name: string) { await delay(); return update(name, { status: "connected", tokenStatus: "valid", lastSync: "Just now", permissions: ["Publish", "Read insights"] }); }
