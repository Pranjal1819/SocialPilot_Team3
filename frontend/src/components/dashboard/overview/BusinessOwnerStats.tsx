"use client";

import { useEffect, useState } from "react";
import StatCard from "@/components/dashboard/StatCard";
import { useCampaignsStore } from "@/store/useCampaignsStore";
import { usePostsStore } from "@/store/usePostsStore";
import { api } from "@/lib/api";

interface AssignedMarketingTeam {
  id: number | string;
  name: string;
}

export default function BusinessOwnerStats() {
  const campaigns = useCampaignsStore((s) => s.campaigns);
  const posts = usePostsStore((s) => s.posts);
  const [marketingTeams, setMarketingTeams] = useState<AssignedMarketingTeam[]>([]);

  const activeCampaigns = campaigns.filter((c) => c.status === "active").length;
  const scheduledPosts = posts.filter((p) => p.status === "scheduled").length;
  const publishedPosts = posts.filter((p) => p.status === "published").length;

  useEffect(() => {
    let active = true;

    api
      .get<AssignedMarketingTeam[]>("/business/my-marketing-team")
      .then(({ data }) => {
        if (active) setMarketingTeams(data);
      })
      .catch(() => {
        if (active) setMarketingTeams([]);
      });

    return () => {
      active = false;
    };
  }, []);

  const teamName = marketingTeams.map((team) => team.name).join(", ");

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
      <StatCard label="Total Campaigns" value={campaigns.length} />
      <StatCard label="Active Campaigns" value={activeCampaigns} />
      <StatCard label="Scheduled Posts" value={scheduledPosts} />
      <StatCard label="Published Posts" value={publishedPosts} />
      <StatCard
        label="Marketing Team"
        value={teamName || "Not assigned"}
        hint={teamName ? undefined : "No team assigned"}
      />
    </div>
  );
}