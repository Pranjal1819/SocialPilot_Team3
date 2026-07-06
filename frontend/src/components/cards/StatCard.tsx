import { LucideIcon, ArrowUpRight } from "lucide-react";

type Variant = "filled" | "light";
type AccentColor = "blue" | "teal" | "amber" | "emerald";

const accentMap: Record<AccentColor, { chip: string; icon: string; fill: string }> = {
  blue: { chip: "bg-blue-50", icon: "text-blue-600", fill: "bg-blue-600" },
  teal: { chip: "bg-teal-50", icon: "text-teal-700", fill: "bg-teal-700" },
  amber: { chip: "bg-amber-50", icon: "text-amber-600", fill: "bg-amber-500" },
  emerald: { chip: "bg-emerald-50", icon: "text-emerald-600", fill: "bg-emerald-500" },
};

interface StatCardProps {
  title: string;
  value: string;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  color?: AccentColor;
  variant?: Variant;
}

export default function StatCard({
  title,
  value,
  icon: Icon,
  trend,
  trendUp = true,
  color = "blue",
  variant = "light",
}: StatCardProps) {
  const accent = accentMap[color];

  if (variant === "filled") {
    return (
      <div className={`relative overflow-hidden rounded-3xl ${accent.fill} p-8 text-white shadow-[0_12px_30px_rgb(0,0,0,0.15)] transition-all duration-200 ease-in-out hover:-translate-y-1`}>
        <div className="flex items-start justify-between">
          <p className="text-sm font-medium text-white/80">{title}</p>
          <button className="flex h-8 w-8 items-center justify-center rounded-full bg-white/15 transition-colors hover:bg-white/25">
            <ArrowUpRight size={16} />
          </button>
        </div>
        <h2 className="mt-6 text-5xl font-bold tracking-tight">{value}</h2>
        {trend && (
          <div className="mt-5 inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1.5 text-xs font-medium">
            <Icon size={13} />
            {trend}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="relative overflow-hidden rounded-3xl border border-slate-100 bg-white p-8 shadow-[0_8px_30px_rgb(0,0,0,0.05)] transition-all duration-200 ease-in-out hover:shadow-[0_12px_40px_rgb(0,0,0,0.09)] hover:-translate-y-1">
      <div className="flex items-start justify-between">
        <div className={`rounded-2xl ${accent.chip} p-4`}>
          <Icon size={26} className={accent.icon} strokeWidth={2} />
        </div>
        <button className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-50 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600">
          <ArrowUpRight size={16} />
        </button>
      </div>

      <p className="mt-7 text-sm font-medium text-slate-500">{title}</p>
      <h2 className="mt-1 text-4xl font-bold tracking-tight text-slate-900">{value}</h2>

      {trend && (
        <span
          className={`mt-4 inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold ${
            trendUp ? "bg-emerald-50 text-emerald-600" : "bg-red-50 text-red-600"
          }`}
        >
          {trendUp ? "+" : ""}
          {trend}
        </span>
      )}
    </div>
  );
}