const API_URL = "http://localhost:8000/api/analytics";
"use client";

import StatCard from "@/components/cards/StatCard";
import { FileText, Link2, Megaphone, TrendingUp, LucideIcon } from "lucide-react";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { Role } from "@/types/user";

interface Stat {
  title: string;
  value: string;
  icon: LucideIcon;
  trend: string;
  trendUp: boolean;
  color: "ocean" | "teal" | "amber" | "emerald";
  variant: "filled" | "light";
  roles: Role[];
}

const allRoles: Role[] = [
  "content_creator",
  "marketing_team",
  "business_user",
  "administrator",
];

const stats: Stat[] = [
  {
    title: "Total Posts",
    value: "24",
    icon: FileText,
    trend: "12.4% this week",
    trendUp: true,
    color: "ocean",
    variant: "filled",
    roles: allRoles,
  },
  {
    title: "Connected Accounts",
    value: "5",
    icon: Link2,
    trend: "2 new",
    trendUp: true,
    color: "teal",
    variant: "light",
    roles: allRoles,
  },
  {
    title: "Campaigns",
    value: "12",
    icon: Megaphone,
    trend: "3.1%",
    trendUp: false,
    color: "amber",
    variant: "light",
    roles: ["marketing_team", "business_user", "administrator"],
  },
  {
    title: "Reach",
    value: "24.5K",
    icon: TrendingUp,
    trend: "18.9% this month",
    trendUp: true,
    color: "emerald",
    variant: "light",
    roles: ["marketing_team", "business_user", "administrator"],
  },
];

export default function DashboardStats() {
  const { role } = useCurrentUser();
  const visibleStats = stats.filter((stat) => stat.roles.includes(role));

  return (
    <div className="grid gap-8 sm:grid-cols-2 xl:grid-cols-4">
      {visibleStats.map((stat) => (
        <StatCard key={stat.title} {...stat} />
      ))}
    </div>
  );
}