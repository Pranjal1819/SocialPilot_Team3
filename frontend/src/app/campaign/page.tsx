"use client";

import Link from "next/link";
import { useState } from "react";

import SearchBar from "@/components/campaign/SearchBar";
import CampaignFilter from "@/components/campaign/CampaignFilter";
import CampaignCard from "@/components/campaign/CampaignCard";
import CampaignStats from "@/components/campaign/CampaignStats";
import DashboardLayout from "@/components/DashboardLayout";

import { mockCampaigns } from "@/lib/mockCampaigns";

export default function CampaignDashboard() {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");

  const filteredCampaigns = mockCampaigns.filter((campaign) => {
    const matchesSearch = campaign.name
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesStatus =
      status === "All" || campaign.status === status;

    return matchesSearch && matchesStatus;
  });
return (

  <DashboardLayout>

    <main className="bg-gray-100 p-8">

      {/* Heading */}

      <div className="mb-10 flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

        <div>

          <h1 className="text-4xl font-bold text-slate-900">
            Campaign Management
          </h1>

          <div className="mt-2 h-1 w-24 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"></div>

        </div>

        <Link
          href="/campaign/create"
          className="rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-3 font-semibold text-white shadow-lg transition duration-300 hover:scale-105 hover:shadow-xl"
        >
          + Create Campaign
        </Link>

      </div>

      {/* Dashboard Statistics */}

      <CampaignStats />

      {/* Search & Filter */}

      <div className="mb-8 flex flex-col gap-4 md:flex-row">

        <SearchBar
          value={search}
          onChange={setSearch}
        />

        <CampaignFilter
          value={status}
          onChange={setStatus}
        />

      </div>

      {/* Campaign Cards */}

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

        {filteredCampaigns.map((campaign) => (
          <CampaignCard
            key={campaign.id}
            campaign={campaign}
          />
        ))}

      </div>

    </main>

  </DashboardLayout>

);
}