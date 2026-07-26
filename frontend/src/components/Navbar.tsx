"use client";

import {
  FaBell,
  FaSearch,
  FaUserCircle,
} from "react-icons/fa";

export default function Navbar() {
  return (
    <header className="flex h-20 items-center justify-between border-b bg-white px-8 shadow-sm">

      {/* Left */}

      <div>

        <h2 className="text-2xl font-bold text-slate-900">
          Campaign Management
        </h2>

        <p className="text-sm text-slate-500">
          Manage campaigns and monitor marketing performance
        </p>

      </div>

      {/* Right */}

      <div className="flex items-center gap-6">

        {/* Search */}

        <div className="relative">

          <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />

          <input
            type="text"
            placeholder="Search..."
            className="rounded-xl border border-slate-200 py-3 pl-11 pr-4 outline-none focus:border-blue-500"
          />

        </div>

        {/* Notifications */}

        <button className="relative rounded-xl bg-slate-100 p-3 transition hover:bg-slate-200">

          <FaBell className="text-xl text-slate-700" />

          <span className="absolute right-2 top-2 h-2.5 w-2.5 rounded-full bg-red-500"></span>

        </button>

        {/* User */}

        <div className="flex items-center gap-3">

          <FaUserCircle className="text-4xl text-blue-600" />

          <div>

            <p className="font-semibold text-slate-900">
              Marketing Team
            </p>

            <p className="text-sm text-slate-500">
              Administrator
            </p>

          </div>

        </div>

      </div>

    </header>
  );
}