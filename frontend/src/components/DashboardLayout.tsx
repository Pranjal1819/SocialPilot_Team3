"use client";

import { ReactNode } from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

interface DashboardLayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  return (
    <div className="flex min-h-screen bg-slate-100">

      {/* Sidebar */}

      <Sidebar />

      {/* Right Section */}

      <div className="flex flex-1 flex-col">

        <Navbar />

        <main className="flex-1 p-8">

          {children}

        </main>

      </div>

    </div>
  );
}