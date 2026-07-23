"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight, Plus, X, CalendarDays } from "lucide-react";

interface CampaignEvent {
  id: string;
  title: string;
  startDate: string;
  endDate: string;
  color: string;
}

const eventColors = ["#0077B6", "#0F766E", "#D97706", "#059669", "#DB2777", "#7C3AED"];

function toISODate(d: Date) {
  return d.toISOString().split("T")[0];
}

function isDateInRange(dateISO: string, startISO: string, endISO: string) {
  return dateISO >= startISO && dateISO <= endISO;
}

export default function CampaignCalendar() {
  const today = new Date();
  const [viewDate, setViewDate] = useState(new Date(today.getFullYear(), today.getMonth(), 1));
  const [events, setEvents] = useState<CampaignEvent[]>([
    {
      id: "1",
      title: "Summer Launch Campaign",
      startDate: toISODate(today),
      endDate: toISODate(new Date(today.getFullYear(), today.getMonth(), today.getDate() + 3)),
      color: eventColors[0],
    },
  ]);
  const [showForm, setShowForm] = useState(false);
  const [formTitle, setFormTitle] = useState("");
  const [formStart, setFormStart] = useState(toISODate(today));
  const [formEnd, setFormEnd] = useState(toISODate(today));

  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const monthLabel = viewDate.toLocaleDateString("en-US", { month: "long", year: "numeric" });

  const goToPrevMonth = () => setViewDate(new Date(year, month - 1, 1));
  const goToNextMonth = () => setViewDate(new Date(year, month + 1, 1));

  const handleAddEvent = () => {
    if (!formTitle.trim()) return;
    const newEvent: CampaignEvent = {
      id: Date.now().toString(),
      title: formTitle,
      startDate: formStart,
      endDate: formEnd < formStart ? formStart : formEnd,
      color: eventColors[events.length % eventColors.length],
    };
    setEvents((prev) => [...prev, newEvent]);
    setFormTitle("");
    setShowForm(false);
  };

  const cells: (number | null)[] = [
    ...Array(firstDayOfMonth).fill(null),
    ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
  ];

  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-[0_8px_22px_-12px_rgba(15,23,42,0.12)]">
      {/* Header band */}
      <div className="flex items-center justify-between bg-gradient-to-r from-[#0096C7] to-[#0077B6] px-6 py-5">
        <div className="flex items-center gap-3 text-white">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white/15">
            <CalendarDays size={18} />
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={goToPrevMonth}
              className="flex h-7 w-7 items-center justify-center rounded-lg hover:bg-white/15 transition-colors"
            >
              <ChevronLeft size={16} />
            </button>
            <h3 className="text-base font-semibold min-w-[140px] text-center">{monthLabel}</h3>
            <button
              onClick={goToNextMonth}
              className="flex h-7 w-7 items-center justify-center rounded-lg hover:bg-white/15 transition-colors"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>

        <button
          onClick={() => setShowForm((v) => !v)}
          className="flex items-center gap-1.5 rounded-lg bg-white px-4 py-2 text-xs font-semibold text-[#0077B6] hover:bg-blue-50 transition-colors"
        >
          <Plus size={14} />
          Add Campaign
        </button>
      </div>

      <div className="p-6">
        {/* Add event form */}
        {showForm && (
          <div className="mb-6 rounded-xl border border-blue-100 bg-blue-50/50 p-5">
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm font-semibold text-slate-800">New campaign</p>
              <button
                onClick={() => setShowForm(false)}
                className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-400 hover:bg-white transition-colors"
              >
                <X size={15} />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-500">Campaign name</label>
                <input
                  type="text"
                  value={formTitle}
                  onChange={(e) => setFormTitle(e.target.value)}
                  placeholder="e.g. Diwali Sale Push"
                  className="mt-1.5 w-full rounded-lg border border-slate-200 bg-white px-3.5 py-2.5 text-sm outline-none focus:border-blue-300 focus:ring-4 focus:ring-blue-50"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-medium text-slate-500">Start date</label>
                  <input
                    type="date"
                    value={formStart}
                    onChange={(e) => setFormStart(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-200 bg-white px-3.5 py-2.5 text-sm outline-none focus:border-blue-300 focus:ring-4 focus:ring-blue-50"
                  />
                </div>
                <div>
                  <label className="text-xs font-medium text-slate-500">End date</label>
                  <input
                    type="date"
                    value={formEnd}
                    onChange={(e) => setFormEnd(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-200 bg-white px-3.5 py-2.5 text-sm outline-none focus:border-blue-300 focus:ring-4 focus:ring-blue-50"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-1">
                <button
                  onClick={() => setShowForm(false)}
                  className="rounded-lg px-4 py-2.5 text-sm font-medium text-slate-500 hover:bg-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAddEvent}
                  className="rounded-lg bg-[#0077B6] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#00618f] transition-colors"
                >
                  Save campaign
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Weekday labels */}
        <div className="grid grid-cols-7 gap-1.5 mb-2">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
            <div key={d} className="text-center text-xs font-semibold text-slate-400 py-1">
              {d}
            </div>
          ))}
        </div>

        {/* Calendar grid */}
        <div className="grid grid-cols-7 gap-1.5">
          {cells.map((day, idx) => {
            if (day === null) return <div key={`empty-${idx}`} />;

            const cellDate = new Date(year, month, day);
            const cellISO = toISODate(cellDate);
            const isToday = cellISO === toISODate(today);
            const isWeekend = cellDate.getDay() === 0 || cellDate.getDay() === 6;
            const dayEvents = events.filter((ev) => isDateInRange(cellISO, ev.startDate, ev.endDate));

            return (
              <div
                key={cellISO}
                className={`min-h-[70px] rounded-xl border p-2 transition-colors ${
                  isToday
                    ? "border-[#0096C7] bg-[#EAF8FC] ring-2 ring-[#CAF0F8]"
                    : isWeekend
                    ? "border-slate-100 bg-slate-50/60"
                    : "border-slate-100 bg-white"
                }`}
              >
                <p
                  className={`text-xs font-semibold ${
                    isToday ? "text-[#0077B6]" : "text-slate-600"
                  }`}
                >
                  {day}
                </p>
                <div className="mt-1 space-y-1">
                  {dayEvents.slice(0, 2).map((ev) => (
                    <div
                      key={ev.id}
                      className="truncate rounded-md px-1.5 py-0.5 text-[10px] font-semibold text-white shadow-sm"
                      style={{ backgroundColor: ev.color }}
                      title={`${ev.title} (${ev.startDate} → ${ev.endDate})`}
                    >
                      {ev.title}
                    </div>
                  ))}
                  {dayEvents.length > 2 && (
                    <p className="text-[10px] font-medium text-slate-400">
                      +{dayEvents.length - 2} more
                    </p>
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