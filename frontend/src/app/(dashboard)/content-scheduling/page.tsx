"use client";

import { useEffect, useMemo, useState } from "react";
import {
  PenSquare,
  CalendarDays,
  FileText,
  ListOrdered,
  Search,
  Filter,
} from "lucide-react";

import CreatePostForm from "@/components/scheduling/CreatePostForm";
import PublishingCalendar from "@/components/scheduling/PublishingCalendar";
import PostList from "@/components/scheduling/PostList";
import TabBar, { TabItem } from "@/components/scheduling/TabBar";
import { ScheduledPost } from "@/types/content";
import {
  deleteScheduledPost,
  getScheduledPosts,
  saveScheduledPost,
} from "@/lib/contentSchedulingService";

type TabKey = "create" | "calendar" | "drafts" | "queue";

export default function ContentSchedulingPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("create");
  const [posts, setPosts] = useState<ScheduledPost[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    getScheduledPosts().then(setPosts);
  }, []);

  const handleSave = async (post: ScheduledPost) => {
    await saveScheduledPost(post);

    setPosts((prev) => [
      ...prev.filter((item) => item.id !== post.id),
      post,
    ]);

    setActiveTab(post.status === "draft" ? "drafts" : "queue");
  };

  const handleDelete = async (id: string) => {
    await deleteScheduledPost(id);

    setPosts((prev) => prev.filter((post) => post.id !== id));
  };

  const drafts = posts.filter((p) => p.status === "draft");

  const queued = posts.filter(
    (p) => p.status === "scheduled" || p.status === "queued"
  );

  const filteredDrafts = drafts.filter((post) =>
    post.caption.toLowerCase().includes(search.toLowerCase())
  );

  const filteredQueue = queued.filter((post) =>
    post.caption.toLowerCase().includes(search.toLowerCase())
  );

  const tabs: TabItem<TabKey>[] = [
    {
      key: "create",
      label: "Create Post",
      icon: PenSquare,
    },
    {
      key: "calendar",
      label: "Calendar",
      icon: CalendarDays,
    },
    {
      key: "drafts",
      label: "Drafts",
      icon: FileText,
      count: drafts.length,
    },
    {
      key: "queue",
      label: "Queue",
      icon: ListOrdered,
      count: queued.length,
    },
  ];

  const stats = useMemo(
    () => [
      {
        title: "Total Posts",
        value: posts.length,
      },
      {
        title: "Scheduled",
        value: posts.filter((p) => p.status === "scheduled").length,
      },
      {
        title: "Drafts",
        value: drafts.length,
      },
      {
        title: "Queue",
        value: queued.length,
      },
    ],
    [posts, drafts.length, queued.length]
  );

  return (
  <div className="mx-auto max-w-[1600px] space-y-8">

    {/* Header */}
    <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900">
          Content Scheduling
        </h1>

        <p className="mt-2 max-w-2xl text-base text-slate-500">
          Create, schedule, organize, and manage your social media content
          across all connected platforms from one place.
        </p>
      </div>
    </div>

    {/* Statistics */}
    <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((item) => (
        <div
          key={item.title}
          className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
        >
          <p className="text-sm font-medium text-slate-500">
            {item.title}
          </p>

          <h2 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
            {item.value}
          </h2>
        </div>
      ))}
    </div>

    {/* Search */}
    {(activeTab === "drafts" || activeTab === "queue") && (
      <div className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm md:flex-row md:items-center md:justify-between">

        <div className="relative w-full md:max-w-md">
          <Search
            size={18}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            type="text"
            placeholder="Search posts..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-11 pr-4 outline-none transition focus:border-cyan-500 focus:bg-white focus:ring-2 focus:ring-cyan-500/20"
          />
        </div>

        <button className="flex items-center justify-center gap-2 rounded-xl border border-slate-200 px-5 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50">
          <Filter size={16} />
          Filter
        </button>
      </div>
    )}

    {/* Tabs */}
    <div className="rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">
      <TabBar
        tabs={tabs}
        active={activeTab}
        onChange={setActiveTab}
      />
    </div>

    {/* Content */}
    <div className="rounded-3xl bg-transparent">
      {activeTab === "create" && (
        <CreatePostForm onSave={handleSave} />
      )}

      {activeTab === "calendar" && (
        <PublishingCalendar posts={posts} />
      )}

      {activeTab === "drafts" && (
        <PostList
          posts={filteredDrafts}
          emptyLabel="No drafts yet. Save a post as draft to see it here."
          onDelete={handleDelete}
        />
      )}

      {activeTab === "queue" && (
        <PostList
          posts={filteredQueue}
          emptyLabel="Nothing scheduled yet. Schedule a post to see it here."
          onDelete={handleDelete}
        />
      )}
    </div>

  </div>
);
}