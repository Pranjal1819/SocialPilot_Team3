import Link from "next/link";
import {
  FaBullhorn,
  FaCalendarCheck,
  FaChartLine,
  FaUsers,
} from "react-icons/fa";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      {/* Hero Section */}
      <section className="mx-auto flex max-w-7xl flex-col items-center justify-center px-6 py-24 text-center">
        <div className="mb-6 inline-flex items-center rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
          SocialPilot • Campaign Management Platform
        </div>

        <h1 className="max-w-4xl text-5xl font-extrabold leading-tight text-slate-900 md:text-6xl">
          Manage Campaigns,
          <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
            {" "}Schedule Posts{" "}
          </span>
          and Track Performance
        </h1>

        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-600 md:text-xl">
          Plan, organize, assign and monitor your social media campaigns from one powerful dashboard.
          Built for marketing teams, content creators and business users.
        </p>

        <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row">
          <Link
            href="/register"
            className="rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-8 py-4 text-lg font-semibold text-white shadow-xl transition hover:scale-105 hover:shadow-2xl"
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="rounded-xl border border-slate-300 bg-white px-8 py-4 text-lg font-semibold text-slate-700 shadow-md transition hover:bg-slate-100"
          >
            Login
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="mx-auto max-w-7xl px-6 py-20">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-slate-900">
            Everything you need for Campaign Management
          </h2>
          <p className="mt-4 text-lg text-slate-600">
            A complete workflow for planning, publishing and tracking social media campaigns.
          </p>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-2xl bg-white p-8 shadow-lg transition hover:-translate-y-2 hover:shadow-2xl">
            <div className="mb-4 inline-flex rounded-xl bg-blue-100 p-4">
              <FaBullhorn className="text-3xl text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Create Campaigns</h3>
            <p className="mt-3 leading-7 text-slate-600">
              Organize multiple posts under one marketing objective.
            </p>
          </div>

          <div className="rounded-2xl bg-white p-8 shadow-lg transition hover:-translate-y-2 hover:shadow-2xl">
            <div className="mb-4 inline-flex rounded-xl bg-cyan-100 p-4">
              <FaCalendarCheck className="text-3xl text-cyan-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Schedule Posts</h3>
            <p className="mt-3 leading-7 text-slate-600">
              Assign and manage posts across platforms.
            </p>
          </div>

          <div className="rounded-2xl bg-white p-8 shadow-lg transition hover:-translate-y-2 hover:shadow-2xl">
            <div className="mb-4 inline-flex rounded-xl bg-purple-100 p-4">
              <FaChartLine className="text-3xl text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Track Progress</h3>
            <p className="mt-3 leading-7 text-slate-600">
              Monitor published, pending and scheduled posts.
            </p>
          </div>

          <div className="rounded-2xl bg-white p-8 shadow-lg transition hover:-translate-y-2 hover:shadow-2xl">
            <div className="mb-4 inline-flex rounded-xl bg-pink-100 p-4">
              <FaUsers className="text-3xl text-pink-600" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Collaborate</h3>
            <p className="mt-3 leading-7 text-slate-600">
              Marketing teams and content creators can work together.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="mx-auto max-w-7xl px-6 pb-24">
        <div className="rounded-3xl bg-gradient-to-r from-blue-600 to-cyan-500 p-10 text-center text-white shadow-2xl md:p-16">
          <h2 className="text-4xl font-bold">
            Ready to manage your campaigns?
          </h2>
          <p className="mt-4 text-lg text-blue-100">
            Start creating, scheduling and tracking campaigns today.
          </p>

          <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/register"
              className="rounded-xl bg-white px-8 py-4 text-lg font-semibold text-blue-600 shadow-lg transition hover:scale-105"
            >
              Create Account
            </Link>

            <Link
              href="/login"
              className="rounded-xl border border-white/40 bg-white/10 px-8 py-4 text-lg font-semibold text-white backdrop-blur transition hover:bg-white/20"
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}