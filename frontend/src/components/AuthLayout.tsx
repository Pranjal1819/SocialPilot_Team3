"use client";

import { ReactNode } from "react";
import { COLORS } from "@/constants/theme";

type AuthLayoutProps = {
  title: string;
  subtitle: string;
  children: ReactNode;
};

export default function AuthLayout({
  title,
  subtitle,
  children,
}: AuthLayoutProps) {
  return (
    <div
      className="min-h-screen flex items-center justify-center px-6 py-10"
      style={{
        backgroundColor: COLORS.authBackground,
      }}
    >
      <div
        className="grid md:grid-cols-2 w-full max-w-6xl overflow-hidden rounded-3xl"
        style={{
          backgroundColor: COLORS.card,
          boxShadow: "0 8px 30px -12px rgba(15,23,42,0.12)",
        }}
      >
        {/* Left Panel */}
        <div
          className="hidden md:flex flex-col justify-center items-center text-white px-12 py-16"
          style={{
            background: `linear-gradient(
  135deg,
  ${COLORS.ocean} 0%,
  ${COLORS.oceanDark} 100%
)`,
          }}
        >
          <h1 className="text-5xl font-bold tracking-tight mb-6">
            SocialPilot
          </h1>

          <p className="text-lg text-center leading-8 opacity-90 max-w-sm">
            Manage all your social media platforms
            <br />
            from one place.
          </p>
        </div>

        {/* Right Panel */}
        <div className="bg-white px-10 py-12 flex flex-col justify-center">

          <h2
            className="text-3xl font-bold tracking-tight mb-3"
            style={{
              color: COLORS.text,
            }}
          >
            {title}
          </h2>

          {subtitle && (
            <p
              className="mb-8"
              style={{
                color: COLORS.body,
              }}
            >
              {subtitle}
            </p>
          )}

          {children}

        </div>
      </div>
    </div>
  );
}