import Link from "next/link";
import {
  FaCalendarAlt,
  FaChartLine,
  FaUsers,
  FaFacebook,
  FaInstagram,
  FaLinkedin,
  FaTwitter,
  FaCheckCircle,
} from "react-icons/fa";

import { COLORS } from "@/constants/theme";

export default function Home() {
  return (
    <main
      className="min-h-screen"
      style={{
        background:
          "linear-gradient(to bottom, #F8FAFC 0%, #EDF7FF 100%)",
      }}
    >
      {/* ================= HERO ================= */}

      <section className="relative overflow-hidden">

        {/* Decorative Circles */}

        <div
          className="absolute -top-24 -left-24 w-72 h-72 rounded-full blur-3xl opacity-20"
          style={{ background: COLORS.ocean }}
        />

        <div
          className="absolute top-10 right-0 w-96 h-96 rounded-full blur-3xl opacity-10"
          style={{ background: COLORS.primary }}
        />

        <div className="max-w-7xl mx-auto px-6 py-20 text-center relative">

          {/* Trusted Badge */}

          <div
            className="inline-flex items-center gap-2 px-5 py-2 rounded-full mb-8"
            style={{
              background: "#EAF6FF",
              color: COLORS.primary,
            }}
          >
            <FaCheckCircle />
            Trusted by 10,000+ marketers
          </div>

          {/* Heading */}

          <h1
            className="text-6xl md:text-7xl font-extrabold leading-tight"
            style={{
              color: COLORS.text,
            }}
          >
            Manage all your
            <br />

            <span
              style={{
                color: COLORS.primary,
              }}
            >
              Social Media
            </span>

            Like a Pro
          </h1>

          {/* Subtitle */}

          <p
            className="max-w-3xl mx-auto mt-8 text-xl leading-9"
            style={{
              color: COLORS.body,
            }}
          >
            Plan, schedule, publish and analyze content across
            Facebook, Instagram, LinkedIn and Twitter from one
            beautiful dashboard.
          </p>

          {/* Buttons */}

          <div className="flex flex-wrap justify-center gap-5 mt-10">

           <Link
  href="/register"
  className="px-8 py-4 rounded-xl text-white font-semibold transition-all duration-300 hover:-translate-y-1 hover:scale-105 hover:shadow-2xl"
              style={{
                background:
                  "linear-gradient(135deg,#0096C7,#0077B6)",
              }}
            >
              Get Started →
            </Link>

           <Link
  href="/login"
  className="px-8 py-4 rounded-xl font-semibold border transition-all duration-300 hover:bg-white hover:scale-105 hover:border-blue-500"
              style={{
                borderColor: COLORS.primary,
                color: COLORS.primary,
              }}
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

          {/* Social Icons */}

<div className="flex justify-center gap-8 mt-12 text-4xl">

  <FaFacebook
    className="hover:scale-125 transition-all duration-300 cursor-pointer"
    style={{ color: "#1877F2" }}
  />

  <FaInstagram
    className="hover:scale-125 transition-all duration-300 cursor-pointer"
    style={{ color: "#E1306C" }}
  />

  <FaLinkedin
    className="hover:scale-125 transition-all duration-300 cursor-pointer"
    style={{ color: "#0A66C2" }}
  />

  <FaTwitter
    className="hover:scale-125 transition-all duration-300 cursor-pointer"
    style={{ color: "#1DA1F2" }}
  />

</div>

        </div>

      </section>
            {/* ================= Statistics ================= */}

      <section className="max-w-6xl mx-auto px-6 -mt-6 mb-20">

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">

          {/* Card 1 */}

          <div
            className="rounded-2xl p-6 text-center hover:-translate-y-2 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
            }}
          >
            <h2
              className="text-4xl font-bold"
              style={{ color: COLORS.primary }}
            >
              100K+
            </h2>

            <p
              className="mt-2"
              style={{ color: COLORS.body }}
            >
              Posts Scheduled
            </p>
          </div>

          {/* Card 2 */}

          <div
            className="rounded-2xl p-6 text-center hover:-translate-y-2 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
            }}
          >
            <h2
              className="text-4xl font-bold"
              style={{ color: COLORS.primary }}
            >
              15K+
            </h2>

            <p
              className="mt-2"
              style={{ color: COLORS.body }}
            >
              Happy Users
            </p>
          </div>

          {/* Card 3 */}

          <div
            className="rounded-2xl p-6 text-center hover:-translate-y-2 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
            }}
          >
            <h2
              className="text-4xl font-bold"
              style={{ color: COLORS.primary }}
            >
              99.9%
            </h2>

            <p
              className="mt-2"
              style={{ color: COLORS.body }}
            >
              Uptime
            </p>
          </div>

          {/* Card 4 */}

          <div
            className="rounded-2xl p-6 text-center hover:-translate-y-2 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
            }}
          >
            <h2
              className="text-4xl font-bold"
              style={{ color: COLORS.primary }}
            >
              24/7
            </h2>

            <p
              className="mt-2"
              style={{ color: COLORS.body }}
            >
              Support
            </p>
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

      <section className="max-w-7xl mx-auto px-6 pb-24">

        <h2
          className="text-5xl font-bold text-center mb-16"
          style={{ color: COLORS.text }}
        >
          Why Choose SocialPilot?
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          {/* Feature 1 */}

          <div
            className="rounded-3xl p-8 hover:-translate-y-3 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 12px 30px rgba(0,0,0,0.05)",
            }}
          >

            <FaCalendarAlt
              size={45}
              style={{ color: COLORS.primary }}
            />

            <h3
              className="text-2xl font-bold mt-6 mb-4"
              style={{ color: COLORS.primary }}
            >
              Schedule Posts
            </h3>

            <p
              className="leading-8"
              style={{ color: COLORS.body }}
            >
              Easily plan, organize and schedule posts across multiple
              social media platforms with one click.
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

          {/* Feature 2 */}

          <div
            className="rounded-3xl p-8 hover:-translate-y-3 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 12px 30px rgba(0,0,0,0.05)",
            }}
          >

            <FaChartLine
              size={45}
              style={{ color: COLORS.primary }}
            />

            <h3
              className="text-2xl font-bold mt-6 mb-4"
              style={{ color: COLORS.primary }}
            >
              Analytics
            </h3>

            <p
              className="leading-8"
              style={{ color: COLORS.body }}
            >
              Monitor audience engagement, campaign reach and performance
              through beautiful analytics dashboards.
            </p>

          </div>

          {/* Feature 3 */}

          <div
            className="rounded-3xl p-8 hover:-translate-y-3 transition-all duration-300"
            style={{
              background: "#F8FCFF",
              border: "1px solid #D6ECFF",
              boxShadow: "0 12px 30px rgba(0,0,0,0.05)",
            }}
          >

            <FaUsers
              size={45}
              style={{ color: COLORS.primary }}
            />

            <h3
              className="text-2xl font-bold mt-6 mb-4"
              style={{ color: COLORS.primary }}
            >
              Team Collaboration
            </h3>

            <p
              className="leading-8"
              style={{ color: COLORS.body }}
            >
              Work together with creators, marketing teams and administrators
              from a single collaborative workspace.
            </p>
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
            {/* ================= CALL TO ACTION ================= */}

      <section
        className="py-24"
        style={{
          background:
            "linear-gradient(135deg,#0096C7 0%, #0077B6 100%)",
        }}
      >
        <div className="max-w-5xl mx-auto text-center px-6">

          <h2
            className="text-5xl font-bold text-white mb-6"
          >
            Ready to Grow Your Brand?
          </h2>

          <p
            className="text-xl text-white/90 max-w-3xl mx-auto leading-9"
          >
            Join thousands of creators and businesses who use
            SocialPilot every day to schedule posts, track analytics
            and collaborate with their teams.
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
              className="px-8 py-4 rounded-xl bg-white font-semibold transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
              style={{
                color: COLORS.primary,
              }}
              className="rounded-xl bg-white px-8 py-4 text-lg font-semibold text-blue-600 transition hover:scale-105"
            >
              Create Free Account
            </Link>

            <Link
              href="/login"
              className="px-8 py-4 rounded-xl border-2 border-white text-white font-semibold transition-all duration-300 hover:bg-white hover:text-sky-700"
              className="rounded-xl border-2 border-white px-8 py-4 text-lg font-semibold text-white transition hover:bg-white hover:text-blue-600"
            >
              Login
            </Link>

          </div>

        </div>

      </section>

      {/* ================= FOOTER ================= */}

      <footer
        className="py-12"
        style={{
          background: COLORS.sidebar,
        }}
      >
        <div className="max-w-7xl mx-auto px-6">

          <div className="grid md:grid-cols-3 gap-10">

            {/* Logo */}

            <div>

              <h2
                className="text-3xl font-bold text-white"
              >
                SocialPilot
              </h2>

              <p
                className="mt-5 leading-8"
                style={{
                  color: "#CBD5E1",
                }}
              >
                Simplify your social media management with one
                unified platform designed for creators,
                marketers and businesses.
              </p>

            </div>

            {/* Quick Links */}

            <div>

              <h3 className="text-xl font-semibold text-white mb-5">
                Quick Links
              </h3>

              <div className="space-y-3">

                <Link
                  href="/"
                  className="block hover:text-white"
                  style={{
                    color: "#CBD5E1",
                  }}
                >
                  Home
                </Link>

                <Link
                  href="/login"
                  className="block hover:text-white"
                  style={{
                    color: "#CBD5E1",
                  }}
                >
                  Login
                </Link>

                <Link
                  href="/register"
                  className="block hover:text-white"
                  style={{
                    color: "#CBD5E1",
                  }}
                >
                  Register
                </Link>

              </div>

            </div>

            {/* Social */}

            <div>

              <h3 className="text-xl font-semibold text-white mb-5">
                Follow Us
              </h3>

              <div className="flex gap-5 text-3xl">

                <FaFacebook
                  className="hover:scale-125 transition cursor-pointer"
                  color="#ffffff"
                />

                <FaInstagram
                  className="hover:scale-125 transition cursor-pointer"
                  color="#ffffff"
                />

                <FaLinkedin
                  className="hover:scale-125 transition cursor-pointer"
                  color="#ffffff"
                />

                <FaTwitter
                  className="hover:scale-125 transition cursor-pointer"
                  color="#ffffff"
                />

              </div>

            </div>

          </div>

          <hr className="my-10 border-slate-700" />

          <p
            className="text-center"
            style={{
              color: "#CBD5E1",
            }}
          >
            © 2026 SocialPilot. All Rights Reserved.
          </p>
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