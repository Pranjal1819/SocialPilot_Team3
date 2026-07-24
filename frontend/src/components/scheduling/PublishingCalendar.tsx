"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight, CalendarDays } from "lucide-react";
import { ScheduledPost } from "@/types/content";
import { contentTypeOptions } from "@/constants/contentTypes";

interface Props {
  posts: ScheduledPost[];
}

function toISODate(d: Date) {
  return d.toISOString().split("T")[0];
}

export default function PublishingCalendar({ posts }: Props) {
  const today = new Date();
  const [viewDate, setViewDate] = useState(new Date(today.getFullYear(), today.getMonth(), 1));

  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const monthLabel = viewDate.toLocaleDateString("en-US", { month: "long", year: "numeric" });

  const cells: (number | null)[] = [
    ...Array(firstDayOfMonth).fill(null),
    ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
  ];

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 px-8 py-6">
        <div className="flex items-center gap-3">
          <CalendarDays size={18} className="text-slate-400" />
          <button
            onClick={() => setViewDate(new Date(year, month - 1, 1))}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100"
          >
            <ChevronLeft size={17} />
          </button>
          <h3 className="min-w-[160px] text-center text-base font-semibold text-slate-900">{monthLabel}</h3>
          <button
            onClick={() => setViewDate(new Date(year, month + 1, 1))}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100"
          >
            <ChevronRight size={17} />
          </button>
        </div>
      </div>

      <div className="p-8">
        <div className="mb-3 grid grid-cols-7 gap-2">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
            <div key={d} className="py-1.5 text-center text-xs font-semibold text-slate-400">
              {d}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 gap-2">
          {cells.map((day, idx) => {
            if (day === null) return <div key={`empty-${idx}`} />;
            const cellISO = toISODate(new Date(year, month, day));
            const isToday = cellISO === toISODate(today);
            const dayPosts = posts.filter((p) => p.scheduledDate === cellISO);

            return (
              <div
                key={cellISO}
                className={`min-h-[92px] rounded-xl border p-2.5 transition-colors ${
                  isToday ? "border-[#0096C7] bg-[#EAF8FC]" : "border-slate-100 bg-white hover:bg-slate-50"
                }`}
              >
                <p className={`text-xs font-semibold ${isToday ? "text-[#0077B6]" : "text-slate-500"}`}>{day}</p>
                <div className="mt-1.5 space-y-1">
                  {dayPosts.slice(0, 2).map((post) => {
                    const typeIcon = contentTypeOptions.find((c) => c.value === post.contentType)?.icon;
                    const Icon = typeIcon;
                    return (
                      <div
                        key={post.id}
                        className="flex items-center gap-1 truncate rounded-md bg-slate-900 px-2 py-1 text-[10px] font-semibold text-white"
                        title={post.caption}
                      >
                        {Icon && <Icon size={10} />}
                        {post.scheduledTime}
                      </div>
                    );
                  })}
                  {dayPosts.length > 2 && (
                    <p className="text-[10px] font-medium text-slate-400">+{dayPosts.length - 2} more</p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}