"use client";

import { COLORS } from "../styles/colors";

type ButtonProps = {
  text: string;
  type?: "button" | "submit";
  loading?: boolean;
};

export default function Button({
  text,
  type = "button",
  loading = false,
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={loading}
      className="w-full py-3 rounded-lg font-semibold text-white shadow-lg transition-all duration-300 hover:scale-[1.02] disabled:cursor-not-allowed disabled:opacity-70"
      style={{
        backgroundColor: loading ? "#94A3B8" : COLORS.secondary,
      }}
    >
      {loading ? "Please wait..." : text}
    </button>
  );
}