import { CheckCircle2 } from "lucide-react";
import { IconType } from "react-icons";

interface PlatformCardProps {
  name: string;
  icon: IconType;
  connected: boolean;
}

export default function PlatformCard({ name, icon: Icon, connected }: PlatformCardProps) {
  return (
    <div
      className={`flex items-center justify-between rounded-2xl border p-5 transition-all duration-200 ease-in-out ${
        connected
          ? "border-slate-100 bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
          : "border-dashed border-slate-200 bg-slate-50/50"
      }`}
    >
      <div className="flex items-center gap-4">
        <div className={`rounded-xl p-3 ${connected ? "bg-blue-50" : "bg-slate-100"}`}>
          <Icon size={22} className={connected ? "text-blue-600" : "text-slate-400"} />
        </div>

        <div>
          <h3 className={`font-semibold ${connected ? "text-slate-900" : "text-slate-500"}`}>
            {name}
          </h3>

          {connected ? (
            <div className="mt-1 flex items-center gap-1.5">
              <CheckCircle2 size={14} className="text-emerald-500" />
              <span className="text-xs font-medium text-emerald-600">Connected</span>
            </div>
          ) : (
            <p className="mt-1 text-xs text-slate-400">Not connected</p>
          )}
        </div>
      </div>

      <button
        className={`rounded-lg px-4 py-2 text-sm font-medium transition-all duration-200 ease-in-out ${
          connected
            ? "text-rose-600 hover:bg-rose-50"
            : "bg-blue-600 text-white hover:bg-blue-700"
        }`}
      >
        {connected ? "Disconnect" : "Connect"}
      </button>
    </div>
  );
}