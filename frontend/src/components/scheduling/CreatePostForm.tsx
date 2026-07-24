"use client";

import { useState } from "react";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import ContentTypeSelector from "./ContentTypeSelector";
import PlatformSelector from "./PlatformSelector";
import ContentPreview from "./ContentPreview";
import DateStrip from "./DateStrip";
import MediaUploader from "./MediaUploader";
import { ContentType, RecurringFrequency, ScheduledPost } from "@/types/content";

interface Props {
  onSave: (post: ScheduledPost, asDraft: boolean) => void;
}

function toISODate(d: Date) {
  return d.toISOString().split("T")[0];
}

export default function CreatePostForm({ onSave }: Props) {
  const [contentType, setContentType] = useState<ContentType>("text");
  const [caption, setCaption] = useState("");
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [mediaFiles, setMediaFiles] = useState<File[]>([]);
  const [date, setDate] = useState(toISODate(new Date()));
  const [time, setTime] = useState("10:00");
  const [recurring, setRecurring] = useState<RecurringFrequency>("none");
  const [error, setError] = useState<string | null>(null);

  const handleContentTypeChange = (type: ContentType) => {
    setContentType(type);
    setMediaFiles([]);
  };

  const buildPost = (status: ScheduledPost["status"]): ScheduledPost => ({
    id: Date.now().toString(),
    caption,
    contentType,
    platforms: selectedPlatforms,
    scheduledDate: date,
    scheduledTime: time,
    status,
    recurring,
    mediaUrls: mediaFiles.map((f) => URL.createObjectURL(f)),
  });

  const handleSaveDraft = () => {
    setError(null);
    onSave(buildPost("draft"), true);
  };

  const handleSchedule = () => {
    if (!caption.trim()) {
      setError("Add a caption before scheduling.");
      return;
    }
    if (selectedPlatforms.length === 0) {
      setError("Select at least one platform to post to.");
      return;
    }

    setError(null);
    onSave(buildPost("scheduled"), false);
    setCaption("");
    setSelectedPlatforms([]);
    setMediaFiles([]);
  };

  return (
  <div className="grid items-start gap-8 xl:grid-cols-[minmax(0,1fr)_380px] 2xl:grid-cols-[minmax(0,1fr)_420px]">
    {/* Composer */}
    <div className="rounded-3xl border border-slate-200 bg-white shadow-lg transition-all duration-300 hover:shadow-xl">
      {/* Header */}
      <div className="border-b border-slate-200 bg-slate-50 px-8 py-6">
        <h2 className="text-lg font-semibold text-slate-900">
          Create New Post
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Fill in the details below.
        </p>
      </div>

      {/* Form */}
      <div className="space-y-6 p-8">

        {/* Content Type */}
        <section className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6">
          <div>
              <h3 className="text-base font-semibold text-slate-900">
                  Content Type
              </h3>
          </div>

          <ContentTypeSelector
            value={contentType}
            onChange={handleContentTypeChange}
          />
        </section>

        {/* Media */}
        {contentType !== "text" && (
          <section className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6">
            <div>
                <h3 className="text-base font-semibold text-slate-900">
                    Upload Media
                </h3>
            </div>

            <MediaUploader
              contentType={contentType}
              files={mediaFiles}
              onChange={setMediaFiles}
            />
          </section>
        )}

        {/* Caption */}
        <section className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-slate-900">
              Caption
            </h3>

            <span
                className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500"
            >
                {caption.length} characters
            </span>
          </div>

          <textarea
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            placeholder="Write your caption..."
            rows={7}
            className="w-full resize-none rounded-xl border border-slate-200 bg-white px-5 py-4 text-base leading-7 shadow-sm outline-none transition-all focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200"
          />
        </section>

        {/* Platforms */}
        <section className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6">
          <div>
            <h3 className="text-base font-semibold text-slate-900">
              Platforms
             </h3>
          </div>

          <PlatformSelector
            value={selectedPlatforms}
            onChange={setSelectedPlatforms}
          />
        </section>

        {/* Schedule */}
        <section className="space-y-6">
          <div>
            <h3 className="text-base font-semibold text-slate-900">
              Publishing Schedule
            </h3>
          </div>

          <div>
            <label className="text-sm font-medium text-slate-600">
              Date
            </label>

            <div className="mt-3">
              <DateStrip value={date} onChange={setDate} />
            </div>
          </div>

          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <label className="text-sm font-medium text-slate-600">
                Time
              </label>

              <input
                type="time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-base outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-600">
                Repeat
              </label>

              <select
                value={recurring}
                onChange={(e) =>
                  setRecurring(e.target.value as RecurringFrequency)
                }
                className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-base outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              >
                <option value="none">Does not repeat</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>
          </div>
        </section>
      </div>

      {error && (
        <div className="mx-8 mb-6 flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      <div className="flex flex-col gap-4 border-t border-slate-200 bg-white px-8 py-6 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-slate-500">
          Ready to publish your content?
        </p>

        <div className="flex flex-col gap-3 sm:flex-row">
          <Button
            variant="outline"
            size="lg"
            className="w-full sm:w-auto"
            onClick={handleSaveDraft}
          >
            Save as Draft
          </Button>

          <Button
            size="lg"
            className="w-full sm:w-auto"
            onClick={handleSchedule}
          >
            Schedule Post
          </Button>
        </div>
      </div>
    </div>

    {/* Preview */}
    <div className="sticky top-6 self-start">
      <ContentPreview
        caption={caption}
        contentType={contentType}
        selectedPlatforms={selectedPlatforms}
        mediaFiles={mediaFiles}
      />
    </div>
  </div>
);
}
