import StatCard from "@/components/cards/StatCard";
import { FileText, Link2, Megaphone, TrendingUp } from "lucide-react";

const stats = [
  { title: "Total Posts", value: "24", icon: FileText, trend: "12.4% this week", trendUp: true, color: "blue" as const, variant: "filled" as const },
  { title: "Connected Accounts", value: "5", icon: Link2, trend: "2 new", trendUp: true, color: "teal" as const, variant: "light" as const },
  { title: "Campaigns", value: "12", icon: Megaphone, trend: "3.1%", trendUp: false, color: "amber" as const, variant: "light" as const },
  { title: "Reach", value: "24.5K", icon: TrendingUp, trend: "18.9% this month", trendUp: true, color: "emerald" as const, variant: "light" as const },
];

export default function DashboardStats() {
  return (
    <div className="grid gap-8 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <StatCard key={stat.title} {...stat} />
      ))}
    </div>
  );
}