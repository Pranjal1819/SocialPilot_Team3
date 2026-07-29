import { CheckCircle2, AlertTriangle } from "lucide-react";
import { IconType } from "react-icons";

export type ConnectionStatus = "connected" | "error" | "disconnected";

interface PlatformCardProps {
  name: string;
  icon: IconType;
  brandColor: string;
  status: ConnectionStatus;
  errorMessage?: string;
}

interface StatusConfig {
  label: string;
  textColor: string;
  showIcon: "check" | "error" | null;
}

const statusConfig: Record<ConnectionStatus, StatusConfig> = {
  connected: {
    label: "Connected",
    textColor: "text-emerald-600",
    showIcon: "check",
  },
  error: {
    label: "Token Expired",
    textColor: "text-red-600",
    showIcon: "error",
  },
  disconnected: {
    label: "Not connected",
    textColor: "text-slate-400",
    showIcon: null,
  },
};

export default function PlatformCard({
  name,
  icon: Icon,
  brandColor,
  status,
  errorMessage,
}: PlatformCardProps) {
  const config = statusConfig[status];
  const isActive = status !== "disconnected";

  return (
    <div className="grid grid-cols-[auto_1fr_160px] items-center gap-5 rounded-2xl border border-slate-100 bg-[#F0F9FC] px-7 py-6 shadow-[0_4px_16px_rgba(15,23,42,0.05)] transition-all duration-200 ease-in-out hover:-translate-y-0.5 hover:shadow-[0_10px_28px_rgba(15,23,42,0.09)]">
      {/* Icon */}
      <div
        className="flex h-14 w-14 items-center justify-center rounded-2xl text-white shadow-sm"
        style={
          brandColor.startsWith("linear-gradient")
            ? { backgroundImage: brandColor }
            : { backgroundColor: brandColor }
        }
      >
        <Icon size={24} />
      </div>

      {/* Name + status */}
      <div className="min-w-0">
        <h3 className={`text-lg font-semibold ${isActive ? "text-slate-900" : "text-slate-500"}`}>
          {name}
        </h3>
        <div className="mt-0.5 flex items-center gap-1.5">
          {config.showIcon === "check" && <CheckCircle2 size={14} className="text-emerald-500 shrink-0" />}
          {config.showIcon === "error" && <AlertTriangle size={14} className="text-red-500 shrink-0" />}
          <span className={`text-xs font-medium ${config.textColor}`}>
            {status === "error" && errorMessage ? errorMessage : config.label}
          </span>
        </div>
      </div>

      {/* Action button */}
      <div className="flex justify-end">
        <button
          className={`w-full rounded-lg px-4 py-2 text-sm font-medium transition-all duration-200 ease-in-out ${
            status === "connected"
              ? "bg-white text-red-600 hover:bg-red-50"
              : status === "error"
              ? "bg-amber-500 text-white hover:bg-amber-600"
              : "bg-blue-600 text-white hover:bg-blue-700"
          }`}
        >
          {status === "connected" ? "Disconnect" : status === "error" ? "Reconnect" : "Connect"}
        </button>
      </div>
    </div>
  );
}