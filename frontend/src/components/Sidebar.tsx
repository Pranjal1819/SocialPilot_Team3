"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  FaTachometerAlt,
  FaBullhorn,
  FaCalendarAlt,
  FaChartLine,
  FaUser,
  FaCog,
  FaSignOutAlt,
} from "react-icons/fa";

export default function Sidebar() {
  const pathname = usePathname();

  const menu = [
    {
      title: "Dashboard",
      href: "/dashboard",
      icon: <FaTachometerAlt />,
    },
    {
      title: "Campaigns",
      href: "/campaign",
      icon: <FaBullhorn />,
    },
    {
      title: "Schedule Posts",
      href: "/campaign/assign-posts",
      icon: <FaCalendarAlt />,
    },
    {
      title: "Analytics",
      href: "/campaign/analytics",
      icon: <FaChartLine />,
    },
    {
      title: "Profile",
      href: "#",
      icon: <FaUser />,
    },
    {
      title: "Settings",
      href: "#",
      icon: <FaCog />,
    },
  ];

  return (
    <aside className="flex h-screen w-72 flex-col bg-slate-900 text-white shadow-xl">

      {/* Logo */}

      <div className="border-b border-slate-700 p-6">

        <h1 className="text-3xl font-extrabold tracking-wide text-cyan-400">

          SocialPilot

        </h1>

        <p className="mt-2 text-sm text-slate-400">

          Marketing Platform

        </p>

      </div>

      {/* Menu */}

      <nav className="flex-1 space-y-2 p-5">

        {menu.map((item) => {

          const active = pathname.startsWith(item.href);

          return (

            <Link
              key={item.title}
              href={item.href}
              className={`flex items-center gap-4 rounded-xl px-5 py-4 transition-all duration-300

              ${
                active
                  ? "bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg"
                  : "hover:bg-slate-800 text-slate-300"
              }`}
            >

              <span className="text-xl">

                {item.icon}

              </span>

              <span className="font-medium">

                {item.title}

              </span>

            </Link>

          );
        })}

      </nav>

      {/* Logout */}

      <div className="border-t border-slate-700 p-5">

        <button className="flex w-full items-center gap-4 rounded-xl bg-red-600 px-5 py-4 font-semibold transition hover:bg-red-700">

          <FaSignOutAlt />

          Logout

        </button>

      </div>

    </aside>
  );
}