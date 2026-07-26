"use client";

import Image from "next/image";
import Link from "next/link";
import {
  FaChartLine,
  FaCalendarAlt,
  FaBullhorn,
  FaArrowRight,
} from "react-icons/fa";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">

      {/* ================= NAVBAR ================= */}

      <nav className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-lg">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

          <div className="flex items-center gap-3">

            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-xl font-bold text-white shadow-lg">
              S
            </div>

            <div>
              <h1 className="text-2xl font-bold text-slate-900">
                SocialPilot
              </h1>

              <p className="text-xs text-slate-500">
                Social Media Management
              </p>
            </div>

          </div>

          <div className="hidden items-center gap-10 font-medium text-slate-600 md:flex">
            <a href="#features" className="transition hover:text-blue-600">
              Features
            </a>

            <a href="#about" className="transition hover:text-blue-600">
              About
            </a>

            <a href="#contact" className="transition hover:text-blue-600">
              Contact
            </a>
          </div>

          <div className="flex items-center gap-4">

            <Link
              href="/login"
              className="rounded-xl border border-slate-300 px-5 py-2 font-semibold text-slate-700 transition hover:border-blue-600 hover:text-blue-600"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-2 font-semibold text-white shadow-lg transition hover:scale-105"
            >
              Register
            </Link>

          </div>

        </div>
      </nav>

      {/* ================= HERO ================= */}

      <section className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-16 px-8 py-20 lg:flex-row">

        <div className="max-w-2xl">

          <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
            🚀 AI Powered Social Media Platform
          </span>

          <h1 className="mt-8 text-6xl font-extrabold leading-tight text-slate-900">
            Manage Your
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              {" "}Social Media
            </span>
            <br />
            Smarter.
          </h1>

          <p className="mt-8 text-xl leading-9 text-slate-600">
            Plan campaigns, schedule posts, collaborate with your team,
            monitor performance and manage all your social media platforms
            from one intelligent dashboard.
          </p>

          <div className="mt-10 flex flex-wrap gap-5">

            <Link
              href="/register"
              className="flex items-center gap-3 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-8 py-4 text-lg font-semibold text-white shadow-xl transition hover:scale-105"
            >
              Get Started
              <FaArrowRight />
            </Link>

            <Link
              href="/login"
              className="rounded-xl border-2 border-slate-300 px-8 py-4 text-lg font-semibold text-slate-700 transition hover:border-blue-600 hover:text-blue-600"
            >
              Login
            </Link>

          </div>

          <div className="mt-14 flex gap-10">

            <div>
              <h2 className="text-4xl font-bold text-blue-600">
                10K+
              </h2>

              <p className="text-slate-600">
                Campaigns Managed
              </p>
            </div>

            <div>
              <h2 className="text-4xl font-bold text-cyan-600">
                99%
              </h2>

              <p className="text-slate-600">
                User Satisfaction
              </p>
            </div>

            <div>
              <h2 className="text-4xl font-bold text-indigo-600">
                24/7
              </h2>

              <p className="text-slate-600">
                Cloud Access
              </p>
            </div>

          </div>

        </div>
                {/* Right Side - Phone Image */}

        <div className="relative flex justify-center">

          {/* Glow Effect */}
          <div className="absolute -z-10 h-[450px] w-[450px] rounded-full bg-gradient-to-r from-cyan-300 via-blue-300 to-indigo-300 opacity-30 blur-3xl"></div>

          <Image
            src="/images/3d-phone.png"
            alt="SocialPilot Dashboard"
            width={520}
            height={620}
            priority
            className="drop-shadow-2xl transition duration-500 hover:scale-105"
          />

        </div>

      </section>

      {/* ================= FEATURES ================= */}

      <section
        id="features"
        className="bg-white py-24"
      >

        <div className="mx-auto max-w-7xl px-8">

          <div className="mb-16 text-center">

            <span className="rounded-full bg-blue-100 px-4 py-2 font-semibold text-blue-700">
              Everything You Need
            </span>

            <h2 className="mt-6 text-5xl font-bold text-slate-900">
              Powerful Features
            </h2>

            <p className="mx-auto mt-6 max-w-3xl text-lg leading-8 text-slate-600">
              SocialPilot helps businesses, marketing teams and content creators
              streamline campaign planning, post scheduling and analytics from a
              single dashboard.
            </p>

          </div>

          <div className="grid gap-8 md:grid-cols-3">

            {/* Card 1 */}

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg transition duration-300 hover:-translate-y-2 hover:shadow-2xl">

              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 text-2xl text-white">
                <FaBullhorn />
              </div>

              <h3 className="mb-4 text-2xl font-bold text-slate-900">
                Campaign Management
              </h3>

              <p className="leading-8 text-slate-600">
                Organize campaigns, manage objectives, budgets, priorities,
                timelines and monitor campaign progress with ease.
              </p>

            </div>

            {/* Card 2 */}

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg transition duration-300 hover:-translate-y-2 hover:shadow-2xl">

              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-r from-indigo-600 to-blue-500 text-2xl text-white">
                <FaCalendarAlt />
              </div>

              <h3 className="mb-4 text-2xl font-bold text-slate-900">
                Smart Scheduling
              </h3>

              <p className="leading-8 text-slate-600">
                Schedule posts across multiple social media platforms with
                calendar-based planning and campaign assignment.
              </p>

            </div>

            {/* Card 3 */}

            <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg transition duration-300 hover:-translate-y-2 hover:shadow-2xl">

              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-500 to-teal-500 text-2xl text-white">
                <FaChartLine />
              </div>

              <h3 className="mb-4 text-2xl font-bold text-slate-900">
                Analytics Dashboard
              </h3>

              <p className="leading-8 text-slate-600">
                Track engagement, reach, impressions, scheduled posts,
                completion percentage and campaign performance.
              </p>

            </div>

          </div>

        </div>

      </section>
            {/* ================= ABOUT ================= */}

      <section
        id="about"
        className="bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 py-24"
      >
        <div className="mx-auto max-w-6xl px-8 text-center">

          <span className="rounded-full bg-cyan-100 px-4 py-2 font-semibold text-cyan-700">
            Why SocialPilot?
          </span>

          <h2 className="mt-6 text-5xl font-bold text-slate-900">
            Simplify Your Marketing Workflow
          </h2>

          <p className="mx-auto mt-8 max-w-4xl text-lg leading-9 text-slate-600">
            Whether you're a business owner, marketing agency or content creator,
            SocialPilot brings campaign management, post scheduling, analytics,
            collaboration and reporting together into one intelligent platform.
            Save time, improve engagement and achieve your marketing goals with
            confidence.
          </p>

        </div>
      </section>

      {/* ================= CALL TO ACTION ================= */}

      <section className="py-24">

        <div className="mx-auto max-w-6xl rounded-[40px] bg-gradient-to-r from-blue-600 via-cyan-500 to-sky-500 px-10 py-20 text-center text-white shadow-2xl">

          <h2 className="text-5xl font-bold">
            Ready to Grow Your Brand?
          </h2>

          <p className="mx-auto mt-6 max-w-3xl text-lg leading-9 text-blue-100">
            Join thousands of marketers using SocialPilot to plan campaigns,
            schedule posts and monitor social media performance from one powerful
            dashboard.
          </p>

          <div className="mt-10 flex flex-wrap justify-center gap-5">

            <Link
              href="/register"
              className="rounded-xl bg-white px-8 py-4 text-lg font-semibold text-blue-600 transition hover:scale-105"
            >
              Create Free Account
            </Link>

            <Link
              href="/login"
              className="rounded-xl border-2 border-white px-8 py-4 text-lg font-semibold text-white transition hover:bg-white hover:text-blue-600"
            >
              Login
            </Link>

          </div>

        </div>

      </section>

      {/* ================= FOOTER ================= */}

      <footer
        id="contact"
        className="border-t border-slate-200 bg-white"
      >

        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 px-8 py-8 md:flex-row">

          <div>

            <h3 className="text-2xl font-bold text-slate-900">
              SocialPilot
            </h3>

            <p className="mt-2 text-slate-500">
              AI Powered Social Media Management Platform
            </p>

          </div>

          <div className="flex gap-8 text-slate-600">

            <a href="#features" className="hover:text-blue-600">
              Features
            </a>

            <a href="#about" className="hover:text-blue-600">
              About
            </a>

            <Link
              href="/login"
              className="hover:text-blue-600"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="hover:text-blue-600"
            >
              Register
            </Link>

          </div>

        </div>

      </footer>

    </main>
  );
}