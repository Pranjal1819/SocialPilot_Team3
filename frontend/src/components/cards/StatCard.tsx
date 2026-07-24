import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";

type AccentColor = "ocean" | "teal" | "amber" | "emerald";

interface AccentStyle {
  chip: string;
  icon: string;
}

const accentMap: Record<AccentColor, AccentStyle> = {
  ocean: { chip: "bg-[#CAF0F8]", icon: "text-[#0077B6]" },
  teal: { chip: "bg-teal-100", icon: "text-teal-700" },
  amber: { chip: "bg-amber-100", icon: "text-amber-600" },
  emerald: { chip: "bg-emerald-100", icon: "text-emerald-600" },
};

interface StatCardProps {
  title: string;
  value: string;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  badge?: string;
  description?: string;
  color?: AccentColor;
}

export default function StatCard({
  title,
  value,
  icon: Icon,
  trend,
  trendUp = true,
  badge,
  description,
  color = "ocean",
}: StatCardProps) {
  const accent = accentMap[color];

  return (
    <div className="flex min-h-[220px] flex-col rounded-2xl border border-slate-100 bg-white p-6 shadow-md transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
      <div className="flex items-start justify-between">
        <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${accent.chip}`}>
          <Icon size={17} className={accent.icon} strokeWidth={2} />
        </div>
        {badge && (
          <Badge variant="secondary" className="gap-1 bg-slate-100 text-slate-600">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
            {badge}
          </Badge>
        )}
      </div>

      <p className="mt-5 text-sm font-medium text-gray-600">{title}</p>
      <h2 className="mt-1.5 text-3xl font-bold leading-none tracking-tight text-slate-900">
        {value}
      </h2>

      {description && <p className="mt-2 text-xs leading-relaxed text-gray-500">{description}</p>}

      {trend && (
        <div
          className={`mt-auto pt-4 inline-flex items-center gap-1 text-xs font-semibold ${
            trendUp ? "text-emerald-600" : "text-red-500"
          }`}
        >
          {trendUp ? <TrendingUp size={13} /> : <TrendingDown size={13} />}
          {trend}
        </div>
      )}
    </div>
  );
}
