"use client";

import { contentTypeOptions } from "@/constants/contentTypes";
import { ContentType } from "@/types/content";
import { ROLE_ACCENTS } from "@/constants/theme";
import { useCurrentUser } from "@/hooks/useCurrentUser";

interface Props {
  value: ContentType;
  onChange: (value: ContentType) => void;
}

export default function ContentTypeSelector({
  value,
  onChange,
}: Props) {
  const { role } = useCurrentUser();
  const accent = ROLE_ACCENTS[role];

  return (
    <div>
      <label className="mb-4 block text-sm font-semibold text-slate-700">
        Content Type
      </label>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 xl:grid-cols-6">
        {contentTypeOptions.map((option) => {
          const Icon = option.icon;
          const isSelected = value === option.value;

          return (
            <button
              key={option.value}
              type="button"
              onClick={() => onChange(option.value)}
              className={`group relative flex min-h-[132px] flex-col items-center justify-center rounded-2xl border bg-white p-5 transition-all duration-300
                ${
                  isSelected
                    ? "scale-[1.02] shadow-lg"
                    : "shadow-sm hover:-translate-y-1 hover:shadow-md"
                }`}
              style={{
                borderColor: isSelected ? accent.solid : "#E2E8F0",
                backgroundColor: isSelected ? accent.soft : "#FFFFFF",
              }}
            >
              {/* Icon */}
              <div
                className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl transition-all duration-300"
                style={{
                  backgroundColor: isSelected
                    ? accent.solid
                    : "#F8FAFC",
                }}
              >
                <Icon
                  size={28}
                  color={isSelected ? "#FFFFFF" : "#94A3B8"}
                />
              </div>

              {/* Label */}
              <span
                className="text-base font-semibold"
                style={{
                  color: isSelected
                    ? accent.text
                    : "#334155",
                }}
              >
                {option.label}
              </span>

              {/* Selected Badge */}
              {isSelected && (
                <span
                  className="absolute right-3 top-3 h-2.5 w-2.5 rounded-full"
                  style={{
                    backgroundColor: accent.solid,
                  }}
                />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}