"use client";

import { useEffect, useState } from "react";
import PlatformCard from "./PlatformCard";
import {
  getSocialAccounts,
  connectPlatform,
  disconnectPlatform,
  refreshToken,
  syncPlatform,
  SocialAccount,
} from "@/lib/socialAccountService";

export default function SocialAccountsList() {
  const [accounts, setAccounts] = useState<SocialAccount[]>([]);
  const [updating, setUpdating] = useState<string | null>(null);

  useEffect(() => {
    getSocialAccounts().then(setAccounts);
  }, []);

  async function run(
    name: string,
    action: (platform: string) => Promise<SocialAccount>
  ) {
    setUpdating(name);

    try {
      const next = await action(name);

      setAccounts((current) =>
        current.map((account) =>
          account.name === name ? next : account
        )
      );
    } finally {
      setUpdating(null);
    }
  }

  return (
  <section className="mx-auto mt-6 max-w-[1500px] px-4 pb-8">
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 xl:grid-cols-3">
      {accounts.map((platform) => (
        <PlatformCard
          key={platform.name}
          {...platform}
          isUpdating={updating === platform.name}
          onConnect={() => run(platform.name, connectPlatform)}
          onDisconnect={() => run(platform.name, disconnectPlatform)}
          onSync={() => run(platform.name, syncPlatform)}
          onRefresh={() => run(platform.name, refreshToken)}
        />
      ))}
    </div>
  </section>
);
}