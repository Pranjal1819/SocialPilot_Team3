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
  badge?: string;
  description?: string;
  color: "ocean" | "teal" | "amber" | "emerald";
  roles: Role[];
}

const allRoles: Role[] = ["content_creator", "marketing_team", "business_user", "administrator"];

const stats: Stat[] = [
  {
    title: "Total Posts",
    value: "24",
    icon: FileText,
    trend: "12.4% this week",
    trendUp: true,
    badge: "Good",
    description: "Across all connected platforms this month.",
    color: "ocean",
    roles: allRoles,
  },
  {
    title: "Connected Accounts",
    value: "5",
    icon: Link2,
    trend: "2 new",
    trendUp: true,
    badge: "Active",
    description: "Facebook, YouTube and 3 others linked.",
    color: "teal",
    roles: allRoles,
  },
  {
    title: "Campaigns",
    value: "12",
    icon: Megaphone,
    trend: "3.1% this month",
    trendUp: false,
    description: "4 running, 8 completed.",
    color: "amber",
    roles: ["marketing_team", "business_user", "administrator"],
  },
  {
    title: "Reach",
    value: "24.5K",
    icon: TrendingUp,
    trend: "18.9% this month",
    trendUp: true,
    badge: "Growing",
    description: "Total impressions across all posts.",
    color: "emerald",
    roles: ["marketing_team", "business_user", "administrator"],
  },
];

export default function DashboardStats() {
  const { role } = useCurrentUser();
  const visibleStats = stats.filter((stat) => stat.roles.includes(role));

  return (
    <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
      {visibleStats.map((stat) => (
        <StatCard key={stat.title} {...stat} />
      ))}
    </div>
  );
}
