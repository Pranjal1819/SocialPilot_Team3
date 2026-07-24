"use client";

import { Check } from "lucide-react";
import { platforms } from "@/constants/platforms";

interface Props {
  value: string[];
  onChange: (value: string[]) => void;
}

export default function PlatformSelector({
  value,
  onChange,
}: Props) {
  const availablePlatforms = platforms;

  const toggle = (name: string) => {
    onChange(
      value.includes(name)
        ? value.filter((v) => v !== name)
        : [...value, name]
    );
  };

  return (
    <div>
      <label className="mb-4 block text-sm font-semibold text-slate-700">
        Select Platforms
      </label>

      {availablePlatforms.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
          <p className="text-sm text-slate-500">
            No connected accounts yet.
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Connect one from the Social Accounts page first.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 xl:grid-cols-6">
          {availablePlatforms.map((platform) => {
            const isSelected = value.includes(platform.name);
            const disabled = platform.status !== "connected";

            const isGradient =
              platform.brandColor.startsWith("linear-gradient");

            return (
              <button
                key={platform.name}
                type="button"
                onClick={() => {
                  if (!disabled) {
                      toggle(platform.name);
                  }
                }}
                className={`relative flex min-h-[125px] flex-col items-center justify-center rounded-2xl border bg-white p-5 transition-all duration-300
                  ${
                    disabled
                      ? "cursor-not-allowed opacity-50 border-slate-200"
                      : isSelected
                      ? "scale-[1.02] border-cyan-500 bg-cyan-50 shadow-lg"
                      : "border-slate-200 shadow-sm hover:-translate-y-1 hover:shadow-md"
                }`}
              >
                {/* Icon */}
                <div
                  className={`relative flex h-16 w-16 items-center justify-center rounded-2xl transition-all duration-300 ${
                    isSelected ? "shadow-md" : ""
                  }`}
                  style={
                    isGradient
                      ? { backgroundImage: platform.brandColor }
                      : { backgroundColor: platform.brandColor }
                  }
                >
                  <platform.icon
                    size={28}
                    className="text-white"
                  />

                  {isSelected && (
                    <span className="absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500 ring-2 ring-white">
                      <Check
                        size={14}
                        strokeWidth={3}
                        className="text-white"
                      />
                    </span>
                  )}
                </div>

                {/* Name */}
                <span
                  className={`mt-4 text-sm font-semibold transition-colors ${
                    isSelected
                      ? "text-slate-900"
                      : "text-slate-600"
                  }`}
                >
                  {platform.name}
                </span>
                <p
                  className={`mt-1 text-xs font-medium ${
                    disabled
                      ? "text-red-500"
                      : "text-emerald-600"
                  }`}
                >
                  {disabled ? "Not Connected" : "Connected"}
                </p>

                {/* Selected Badge */}
                {isSelected && (
                  <span className="mt-2 rounded-full bg-cyan-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-cyan-700">
                    Selected
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}