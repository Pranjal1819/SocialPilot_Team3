"use client";

import Link from "next/link";
import { useState } from "react";
import {
  FaBullhorn,
  FaCalendarAlt,
  FaRupeeSign,
  FaClipboardList,
  FaAlignLeft,
  FaGlobe,
  FaBullseye,
  FaLayerGroup,
  FaArrowLeft,
} from "react-icons/fa";

export default function CampaignForm() {
  const [formData, setFormData] = useState({
    name: "",
    objective: "",
    platform: "Instagram",
    type: "Product Launch",
    budget: "",
    startDate: "",
    endDate: "",
    totalPosts: "",
    status: "Draft",
    description: "",
  });

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    console.log(formData);

    alert("Campaign Created Successfully! (Mock)");
  };

  return (
    <div className="mx-auto max-w-6xl">

      {/* Back Button */}

      <Link
        href="/campaign"
        className="mb-6 inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:bg-slate-100"
      >
        <FaArrowLeft />
        Back to Dashboard
      </Link>

      {/* Header */}

      <div className="mb-10">

        <h1 className="text-4xl font-bold text-slate-900">
          Create New Campaign
        </h1>

        <p className="mt-2 text-slate-500">
          Plan, schedule and manage campaigns across multiple social media
          platforms.
        </p>

        <div className="mt-4 h-1 w-28 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"></div>

      </div>

      <form
        onSubmit={handleSubmit}
        className="rounded-3xl border border-slate-200 bg-white p-10 shadow-2xl"
      >

        {/* Campaign Information */}

        <div className="mb-12">

          <div className="mb-6 flex items-center gap-3">

            <div className="rounded-xl bg-blue-100 p-3">
              <FaBullhorn className="text-xl text-blue-600" />
            </div>

            <div>

              <h2 className="text-xl font-bold text-slate-800">
                Campaign Information
              </h2>

              <p className="text-sm text-slate-500">
                Basic information about your campaign.
              </p>

            </div>

          </div>

          <div className="grid gap-8 md:grid-cols-2">

            {/* Campaign Name */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Campaign Name
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-blue-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-100">

                <FaBullhorn className="text-lg text-blue-600" />

                <input
                  type="text"
                  name="name"
                  placeholder="Summer Sale 2026"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                  required
                />

              </div>

            </div>

            {/* Budget */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Budget
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-emerald-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-emerald-100">

                <FaRupeeSign className="text-lg text-emerald-600" />

                <input
                  type="number"
                  name="budget"
                  placeholder="200000"
                  value={formData.budget}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                />

              </div>

            </div>

            {/* Objective */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Objective
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-purple-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-purple-100">

                <FaBullseye className="text-lg text-purple-600" />

                <input
                  type="text"
                  name="objective"
                  placeholder="Increase Brand Awareness"
                  value={formData.objective}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                />

              </div>

            </div>

            {/* Platform */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Platform
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-indigo-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-indigo-100">

                <FaGlobe className="text-lg text-indigo-600" />

                <select
                  name="platform"
                  value={formData.platform}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                >
                  <option>Instagram</option>
                  <option>Facebook</option>
                  <option>LinkedIn</option>
                  <option>X</option>
                  <option>YouTube</option>
                </select>

              </div>

            </div>
                      </div>

        </div>

        {/* Schedule & Budget */}

        <div className="mb-12">

          <div className="mb-6 flex items-center gap-3">

            <div className="rounded-xl bg-emerald-100 p-3">
              <FaLayerGroup className="text-xl text-emerald-600" />
            </div>

            <div>

              <h2 className="text-xl font-bold text-slate-800">
                Schedule & Budget
              </h2>

              <p className="text-sm text-slate-500">
                Configure campaign schedule and execution details.
              </p>

            </div>

          </div>

          <div className="grid gap-8 md:grid-cols-2">

            {/* Campaign Type */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Campaign Type
              </label>

              <select
                name="type"
                value={formData.type}
                onChange={handleChange}
                className="w-full rounded-xl border border-slate-300 bg-slate-50 p-4 outline-none transition-all focus:border-orange-500 focus:bg-white focus:ring-2 focus:ring-orange-100"
              >
                <option>Product Launch</option>
                <option>Brand Awareness</option>
                <option>Sales Promotion</option>
                <option>Festival Campaign</option>
              </select>

            </div>

            {/* Status */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Status
              </label>

              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full rounded-xl border border-slate-300 bg-slate-50 p-4 outline-none transition-all focus:border-yellow-500 focus:bg-white focus:ring-2 focus:ring-yellow-100"
              >
                <option>Draft</option>
                <option>Running</option>
                <option>Completed</option>
              </select>

            </div>

            {/* Start Date */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Start Date
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-green-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-green-100">

                <FaCalendarAlt className="text-lg text-green-600" />

                <input
                  type="date"
                  name="startDate"
                  value={formData.startDate}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                />

              </div>

            </div>

            {/* End Date */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                End Date
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-rose-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-rose-100">

                <FaCalendarAlt className="text-lg text-rose-500" />

                <input
                  type="date"
                  name="endDate"
                  value={formData.endDate}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                />

              </div>

            </div>

          </div>

        </div>

        {/* Content Planning */}

        <div>

          <div className="mb-6 flex items-center gap-3">

            <div className="rounded-xl bg-violet-100 p-3">
              <FaClipboardList className="text-xl text-violet-600" />
            </div>

            <div>

              <h2 className="text-xl font-bold text-slate-800">
                Content Planning
              </h2>

              <p className="text-sm text-slate-500">
                Define content volume and campaign description.
              </p>

            </div>

          </div>

          <div className="grid gap-8">

            {/* Total Posts */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Total Posts
              </label>

              <div className="flex items-center rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-indigo-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-indigo-100">

                <FaClipboardList className="text-lg text-indigo-600" />

                <input
                  type="number"
                  name="totalPosts"
                  placeholder="20"
                  value={formData.totalPosts}
                  onChange={handleChange}
                  className="w-full bg-transparent p-4 outline-none"
                />

              </div>

            </div>

            {/* Description */}

            <div>

              <label className="mb-2 block font-semibold text-slate-700">
                Description
              </label>

              <div className="flex rounded-xl border border-slate-300 bg-slate-50 px-4 transition-all focus-within:border-pink-500 focus-within:bg-white focus-within:ring-2 focus-within:ring-pink-100">

                <FaAlignLeft className="mt-5 text-lg text-pink-500" />

                <textarea
                  rows={6}
                  name="description"
                  placeholder="Describe campaign goals, target audience, hashtags, strategy and important notes..."
                  value={formData.description}
                  onChange={handleChange}
                  className="w-full resize-none bg-transparent p-4 outline-none"
                />

              </div>

              <p className="mt-2 text-sm text-slate-500">
                Tip: Include campaign goals, audience, hashtags and content strategy.
              </p>

            </div>
                      </div>

        </div>

        {/* Action Buttons */}

        <div className="mt-12 flex flex-col-reverse gap-4 border-t border-slate-200 pt-8 sm:flex-row sm:justify-end">

          <Link href="/campaign">

            <button
              type="button"
              className="rounded-xl border border-slate-300 bg-white px-8 py-3 font-semibold text-slate-700 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:bg-slate-100 hover:shadow-md"
            >
              Cancel
            </button>

          </Link>

          <button
            type="submit"
            className="rounded-xl bg-gradient-to-r from-blue-600 via-sky-500 to-cyan-500 px-10 py-3 font-semibold text-white shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
          >
            🚀 Create Campaign
          </button>

        </div>

      </form>

    </div>
  );
}