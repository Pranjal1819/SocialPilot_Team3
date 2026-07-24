import {
  CheckCircle2,
  AlertTriangle,
  Clock3,
  ShieldCheck,
} from "lucide-react";
import { IconType } from "react-icons";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export type ConnectionStatus =
  | "connected"
  | "error"
  | "disconnected";

interface PlatformCardProps {
  name: string;
  icon: IconType;
  brandColor: string;
  status: ConnectionStatus;
  errorMessage?: string;
  lastSync?: string | null;
  permissions?: string[];
  tokenStatus?:
    | "valid"
    | "expired"
    | "needs_refresh"
    | "not_connected";
  isUpdating?: boolean;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onSync?: () => void;
  onRefresh?: () => void;
}

export default function PlatformCard({
  name,
  icon: Icon,
  brandColor,
  status,
  errorMessage,
  lastSync,
  permissions = [],
  tokenStatus,
  isUpdating,
  onConnect,
  onDisconnect,
  onSync,
  onRefresh,
}: PlatformCardProps) {
  const isGradient = brandColor.startsWith("linear-gradient");

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-md transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">

      {/* Header */}

      <div className="flex items-center gap-4 p-6">

        <div
          className="flex h-16 w-16 items-center justify-center rounded-2xl text-white shadow-sm"
          style={
            isGradient
              ? { backgroundImage: brandColor }
              : { backgroundColor: brandColor }
          }
        >
          <Icon size={30} />
        </div>

        <div className="flex-1">

          <h3 className="text-2xl font-bold text-slate-900">
            {name}
          </h3>

          <div className="mt-2">

            {status === "connected" && (
              <Badge className="bg-green-100 text-green-700">
                <CheckCircle2 size={14} />
                Connected
              </Badge>
            )}

            {status === "error" && (
              <Badge className="bg-yellow-100 text-yellow-700">
                <AlertTriangle size={14} />
                Token Expired
              </Badge>
            )}

            {status === "disconnected" && (
              <Badge variant="secondary">
                Not Connected
              </Badge>
            )}

          </div>

        </div>

      </div>

      <div className="border-t border-slate-100" />

      {/* Body */}

      <div className="space-y-4 px-6 py-5">

        {/* Last Sync */}

        <div>

          <p className="text-[11px] font-bold uppercase tracking-widest text-slate-400">
            Last Sync
          </p>

          <div className="mt-2 flex items-center gap-2 text-sm text-slate-700">

            <Clock3 size={15} />

            {lastSync ?? "Never"}

          </div>

        </div>

        {/* Token */}

        <div>

          <p className="text-[11px] font-bold uppercase tracking-widest text-slate-400">
            Token Status
          </p>

          <p
            className={`mt-2 text-sm font-semibold ${
              tokenStatus === "valid"
                ? "text-green-600"
                : tokenStatus === "expired"
                ? "text-red-600"
                : "text-slate-500"
            }`}
          >
            {tokenStatus
              ? tokenStatus.replace("_", " ")
              : "Not Connected"}
          </p>

        </div>

        {/* Permissions */}

        <div>

          <p className="text-[11px] font-bold uppercase tracking-widest text-slate-400">
            Permissions
          </p>

          <div className="mt-2 flex min-h-[32px] flex-wrap gap-2">

            {permissions.length ? (
              permissions.map((permission) => (
                <Badge
                  key={permission}
                  variant="secondary"
                  className="rounded-full"
                >
                  <ShieldCheck size={12} />
                  {permission}
                </Badge>
              ))
            ) : (
              <span className="text-sm text-slate-400">
                No permissions granted
              </span>
            )}

          </div>

        </div>

        {/* Error */}

        <div className="h-10">

          {status === "error" && (

            <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
              {errorMessage ?? "Token expired"}
            </div>

          )}

        </div>

      </div>

      {/* Footer */}

      <div className="flex justify-center gap-3 border-t border-slate-100 px-6 py-5">

        {status === "connected" && (

          <Button
            variant="outline"
            size="sm"
            className="h-10 w-32 rounded-xl"
            onClick={onSync}
            disabled={isUpdating}
          >
            Sync
          </Button>

        )}

        <Button
          size="sm"
          className="h-10 w-36 rounded-xl"
          variant={
            status === "connected"
              ? "destructive"
              : "default"
          }
          onClick={
            status === "connected"
              ? onDisconnect
              : status === "error"
              ? onRefresh
              : onConnect
          }
          disabled={isUpdating}
        >
          {isUpdating
            ? "Updating..."
            : status === "connected"
            ? "Disconnect"
            : status === "error"
            ? "Reconnect"
            : "Connect"}
        </Button>

      </div>

    </div>
  );
}