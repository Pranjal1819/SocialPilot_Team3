"use client";

import Link from "next/link";
import { useState } from "react";
import { useParams } from "next/navigation";
import DashboardLayout from "@/components/DashboardLayout";

import {
  FaArrowLeft,
  FaBullhorn,
  FaSave,
} from "react-icons/fa";

export default function EditCampaignPage() {
  const params = useParams();

  const campaignId = params.id;

  const [name, setName] = useState("Nike Summer Sale");
  const [description, setDescription] = useState(
    "Promote the latest summer collection across all social media platforms."
  );
  const [objective, setObjective] = useState("Product Launch");
  const [budget, setBudget] = useState("200000");
  const [category, setCategory] = useState("Marketing");
  const [priority, setPriority] = useState("High");
  const [startDate, setStartDate] = useState("2026-07-01");
  const [endDate, setEndDate] = useState("2026-07-31");

  function handleSave(e: React.FormEvent) {
    e.preventDefault();

    alert("Campaign updated successfully!");
  }

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
        <div className="mx-auto max-w-5xl">

          {/* Header */}

          <Link
            href={`/campaign/${campaignId}`}
            className="mb-6 inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 shadow hover:bg-slate-100"
          >
            <FaArrowLeft />
            Back to Campaign
          </Link>

          <div className="mb-10">

            <div className="flex items-center gap-4">

              <div className="rounded-xl bg-blue-100 p-4">
                <FaBullhorn className="text-2xl text-blue-600" />
              </div>

              <div>

                <h1 className="text-4xl font-bold text-slate-900">
                  Edit Campaign
                </h1>

                <p className="mt-2 text-slate-600">
                  Update campaign details and save your changes.
                </p>

              </div>

            </div>

            <div className="mt-4 h-1 w-24 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"></div>

          </div>

          {/* Form */}

          <form
            onSubmit={handleSave}
            className="rounded-2xl bg-white p-8 shadow-xl"
          >

            <div className="grid gap-6 md:grid-cols-2">

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  Campaign Name
                </label>

                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  Objective
                </label>

                <input
                  type="text"
                  value={objective}
                  onChange={(e) => setObjective(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                />

              </div>

              <div className="md:col-span-2">

                <label className="mb-2 block font-semibold text-slate-700">
                  Description
                </label>

                <textarea
                  rows={4}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  Budget (₹)
                </label>

                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  Category
                </label>

                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                >
                  <option>Marketing</option>
                  <option>Promotion</option>
                  <option>Education</option>
                  <option>Sales</option>
                </select>

              </div>

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  Priority
                </label>

                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                >
                  <option>High</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>

              </div>

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  Start Date
                </label>

                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                />

              </div>

              <div>

                <label className="mb-2 block font-semibold text-slate-700">
                  End Date
                </label>

                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 p-3 focus:border-blue-500 focus:outline-none"
                />

              </div>

            </div>

            {/* Buttons */}

            <div className="mt-10 flex flex-wrap gap-4">

              <button
                type="submit"
                className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-8 py-3 font-semibold text-white transition hover:scale-105"
              >
                <FaSave />
                Save Changes
              </button>

              <Link
                href={`/campaign/${campaignId}`}
                className="rounded-xl border border-slate-300 px-8 py-3 font-semibold text-slate-700 transition hover:bg-slate-100"
              >
                Cancel
              </Link>

            </div>

          </form>

        </div>
      </div>
    </DashboardLayout>
  );
}