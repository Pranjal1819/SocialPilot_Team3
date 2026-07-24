import { PlusIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { platforms } from "@/constants/platforms";

export default function SocialAccountsHeader() {
  const connectedCount = platforms.filter(
    (p) => p.status === "connected"
  ).length;

  return (
    <div className="mb-8 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
      {/* Left Section */}
      <div className="max-w-3xl">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900">
          Connect &amp; Manage Social Media Accounts
        </h1>

        <p className="mt-3 text-lg text-slate-600">
          Connect, disconnect, and monitor all your connected social platforms.
        </p>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3">
        <span className="rounded-full bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-700">
          {connectedCount} of {platforms.length} Connected
        </span>

        <Button className="h-11 px-6">
          <PlusIcon className="h-4 w-4" />
          Connect Account
        </Button>
      </div>
    </div>
  );
}