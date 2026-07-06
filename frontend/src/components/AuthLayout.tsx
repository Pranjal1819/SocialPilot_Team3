"use client";

import { ReactNode } from "react";
import { COLORS } from "../styles/colors";

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
      className="min-h-screen flex items-center justify-center p-6"
      style={{ backgroundColor: COLORS.background }}
    >
      <div className="grid md:grid-cols-2 w-full max-w-5xl bg-white rounded-3xl shadow-2xl overflow-hidden">
        
        {/* Left Side */}
        <div
          className="hidden md:flex flex-col justify-center items-center p-10 text-white"
          style={{ backgroundColor: COLORS.primary }}
        >
          <h1 className="text-5xl font-bold mb-4">
            SocialPilot
          </h1>

          <p className="text-center text-lg opacity-90">
            Manage all your social media platforms
            from one place.
          </p>
        </div>

        {/* Right Side */}
        <div className="p-10 flex flex-col justify-center">

          <h2
            className="text-3xl font-bold mb-2"
            style={{ color: COLORS.primary }}
          >
            {title}
          </h2>

          <p
            className="mb-8"
            style={{ color: COLORS.text }}
          >
            {subtitle}
          </p>

          {children}

        </div>

      </div>
    </div>
  );
}