"use client";

import { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";
import StatCard from "@/components/dashboard/StatCard";
import { ROLE_LABELS, ROLE_VALUES, type Role } from "@/lib/validation";

interface UserMetric {
  user_id: number;
  name: string;
  role: Role;
  total_posts: number;
  published_posts: number;
  total_engagement: number;
  reach: number;
}

interface AnalyticsResponse {
  totals: Record<string, number>;
  users: UserMetric[];
  platforms: { platform: string; posts: number; engagement: number; reach: number; impressions: number }[];
}

export default function AdministratorAnalytics() {
  const [role, setRole] = useState<Role | "all">("all");
  const [userId, setUserId] = useState("all");
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<AnalyticsResponse>("/admin/analytics").then((response) => setData(response.data)).finally(() => setLoading(false));
  }, []);

  const rows = useMemo(
    () => (data?.users ?? []).filter((user) => (role === "all" || user.role === role) && (userId === "all" || String(user.user_id) === userId)),
    [data, role, userId]
  );

  if (loading) return <p className="text-sm text-muted">Loading analytics…</p>;

  const totals = data?.totals ?? {};
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-xl font-bold">Platform Analytics</h1>
        <p className="mt-1 text-sm text-muted">Database-backed activity across every user.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Users" value={totals.total_users ?? 0} />
        <StatCard label="Business Owners" value={totals.business_owners ?? 0} />
        <StatCard label="Marketing Teams" value={totals.marketing_teams ?? 0} />
        <StatCard label="Content Creators" value={totals.content_creators ?? 0} />
        <StatCard label="Total Posts" value={totals.total_posts ?? 0} />
        <StatCard label="Total Engagement" value={totals.total_engagement ?? 0} />
      </div>

      <div className="flex flex-wrap gap-2">
        <select value={role} onChange={(event) => setRole(event.target.value as Role | "all")} className="border border-border bg-surface px-3 py-2 text-sm">
          <option value="all">All roles</option>
          {ROLE_VALUES.map((value) => <option key={value} value={value}>{ROLE_LABELS[value]}</option>)}
        </select>
        <select value={userId} onChange={(event) => setUserId(event.target.value)} className="border border-border bg-surface px-3 py-2 text-sm">
          <option value="all">All users</option>
          {(data?.users ?? []).map((user) => <option key={user.user_id} value={user.user_id}>{user.name}</option>)}
        </select>
      </div>

      <div className="border border-border bg-surface p-5">
        <p className="font-mono text-xs text-muted">POSTS AND ENGAGEMENT BY USER</p>
        <div className="mt-4 h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={rows} margin={{ left: 8, right: 8 }}>
              <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="total_posts" name="Posts" fill="#d99b00" />
              <Bar dataKey="total_engagement" name="Engagement" fill="#3e6da3" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="border border-border bg-surface p-5">
        <p className="font-mono text-xs text-muted">PLATFORM PERFORMANCE</p>
        <div className="mt-4 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data?.platforms ?? []}>
              <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
              <XAxis dataKey="platform" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="engagement" name="Engagement" fill="#d99b00" />
              <Bar dataKey="reach" name="Reach" fill="#3f6b4e" />
              <Bar dataKey="impressions" name="Impressions" fill="#a8452f" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}