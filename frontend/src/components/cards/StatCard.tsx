import { LucideIcon, ArrowUpRight } from "lucide-react";

type Variant = "filled" | "light";
type AccentColor = "ocean" | "teal" | "amber" | "emerald";

interface AccentStyle {
  bg: string;
  chip: string;
  icon: string;
  fill: string;
  shadow: string;
}

const accentMap: Record<AccentColor, AccentStyle> = {
  ocean: {
    bg: "bg-[#CAF0F8]/40",
    chip: "bg-[#ADE8F4]",
    icon: "text-[#0077B6]",
    fill: "bg-gradient-to-br from-[#0096C7] to-[#0077B6]",
    shadow:
      "shadow-[0_12px_30px_-10px_rgba(0,119,182,0.4)] hover:shadow-[0_16px_38px_-8px_rgba(0,119,182,0.45)]",
  },
  teal: {
    bg: "bg-teal-50/60",
    chip: "bg-teal-100",
    icon: "text-teal-700",
    fill: "bg-gradient-to-br from-teal-500 to-teal-800",
    shadow:
      "shadow-[0_12px_30px_-10px_rgba(15,118,110,0.4)] hover:shadow-[0_16px_38px_-8px_rgba(15,118,110,0.45)]",
  },
  amber: {
    bg: "bg-amber-50/60",
    chip: "bg-amber-100",
    icon: "text-amber-600",
    fill: "bg-gradient-to-br from-amber-400 to-orange-600",
    shadow:
      "shadow-[0_12px_30px_-10px_rgba(217,119,6,0.35)] hover:shadow-[0_16px_38px_-8px_rgba(217,119,6,0.4)]",
  },
  emerald: {
    bg: "bg-emerald-50/60",
    chip: "bg-emerald-100",
    icon: "text-emerald-600",
    fill: "bg-gradient-to-br from-emerald-500 to-emerald-800",
    shadow:
      "shadow-[0_12px_30px_-10px_rgba(4,120,87,0.4)] hover:shadow-[0_16px_38px_-8px_rgba(4,120,87,0.45)]",
  },
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
  color = "ocean",
  variant = "light",
}: StatCardProps) {
  const accent = accentMap[color];

  if (variant === "filled") {
    return (
      <div
        className={`relative overflow-hidden rounded-2xl ${accent.fill} p-5 min-h-[130px] flex flex-col justify-between text-white transition-all duration-200 ease-in-out hover:-translate-y-1 ${accent.shadow}`}
      >
        <div className="flex items-start justify-between">
          <p className="text-xs font-medium text-white/85">{title}</p>
          <button className="flex h-7 w-7 items-center justify-center rounded-full bg-white/15 transition-colors hover:bg-white/25">
            <ArrowUpRight size={14} />
          </button>
        </div>

        <h2 className="text-3xl font-bold tracking-tight">{value}</h2>

        {trend && (
          <div className="inline-flex w-fit items-center gap-1.5 rounded-full bg-white/20 px-2.5 py-1 text-xs font-semibold">
            <Icon size={11} />
            {trend}
          </div>
        )}
      </div>
    );
  }

  return (
    <div
      className={`relative overflow-hidden rounded-2xl border border-slate-100 ${accent.bg} p-5 min-h-[130px] flex flex-col justify-between transition-all duration-200 ease-in-out hover:-translate-y-1 shadow-[0_8px_22px_-12px_rgba(15,23,42,0.12)] hover:shadow-[0_12px_30px_-10px_rgba(15,23,42,0.16)]`}
    >
      <div className="flex items-start justify-between">
        <div className={`rounded-lg ${accent.chip} p-2.5`}>
          <Icon size={18} className={accent.icon} strokeWidth={2} />
        </div>
        <button className="flex h-7 w-7 items-center justify-center rounded-full bg-white/70 text-slate-400 transition-colors hover:bg-white hover:text-slate-600">
          <ArrowUpRight size={14} />
        </button>
      </div>

      <div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">{value}</h2>
        <p className="mt-1 text-xs font-medium text-slate-600">{title}</p>

        {trend && (
          <span
            className={`mt-2 inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-bold ${
              trendUp
                ? "border-emerald-200 bg-emerald-100 text-emerald-700"
                : "border-red-200 bg-red-100 text-red-700"
            }`}
          >
            {trendUp ? "+" : ""}
            {trend}
          </span>
        )}
      </div>
    </div>
  );
}