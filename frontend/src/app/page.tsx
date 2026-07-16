import Link from "next/link";
import Image from "next/image";

import {
  FaCalendarAlt,
  FaChartLine,
  FaUsers,
  FaFacebook,
  FaInstagram,
  FaLinkedin,
  FaPinterest,
  FaYoutube,
  FaCheckCircle,
} from "react-icons/fa";

import { FaXTwitter } from "react-icons/fa6";

import { COLORS } from "@/constants/theme";

export default function Home() {
  return (
    <main
      className="min-h-screen"
      style={{
        background:
          "linear-gradient(to bottom,#F8FAFC 0%,#EDF7FF 100%)",
      }}
    >

      {/* ================= HEADER ================= */}

      <header className="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">

        <h2
          className="text-3xl font-bold tracking-tight"
          style={{ color: COLORS.primary }}
        >
          SocialPilot
        </h2>

        <nav className="flex items-center gap-5">

          <Link
            href="/"
            className="font-medium hover:text-sky-700 transition"
            style={{ color: COLORS.body }}
          >
            Home
          </Link>

          <Link
            href="/login"
            className="font-medium hover:text-sky-700 transition"
            style={{ color: COLORS.body }}
          >
            Login
          </Link>

          <Link
            href="/register"
            className="px-6 py-2 rounded-full text-white font-semibold transition-all duration-300 hover:scale-105"
            style={{
              background:
                "linear-gradient(135deg,#0096C7,#0077B6)",
            }}
          >
            Register
          </Link>

        </nav>

      </header>

      {/* ================= HERO ================= */}

      <section className="relative overflow-hidden">

        <div
          className="absolute -top-24 -left-24 w-80 h-80 rounded-full blur-3xl opacity-20"
          style={{ background: COLORS.ocean }}
        />

        <div
          className="absolute top-10 right-0 w-96 h-96 rounded-full blur-3xl opacity-10"
          style={{ background: COLORS.primary }}
        />

        <div className="max-w-7xl mx-auto px-6 py-20 text-center relative">

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

          <h1
            className="text-6xl md:text-7xl font-extrabold leading-tight"
            style={{
              color: COLORS.text,
            }}
          >
            Manage all your

            <br />

            <span style={{ color: COLORS.primary }}>
              Social Media
            </span>

            <br />

            Like a Pro
          </h1>

          <p
            className="max-w-3xl mx-auto mt-8 text-xl leading-9"
            style={{
              color: COLORS.body,
            }}
          >
            Plan, publish, schedule and analyze content across
            Facebook, Instagram, LinkedIn, X, Pinterest and
            YouTube from one beautiful dashboard.
          </p>

          <div className="flex justify-center gap-5 mt-10">

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

          </div>

          {/* Social Apps */}

          <div className="flex justify-center gap-8 mt-14 text-4xl">

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

            <FaXTwitter
              className="hover:scale-125 transition-all duration-300 cursor-pointer"
              style={{ color: "#111827" }}
            />

            <FaPinterest
              className="hover:scale-125 transition-all duration-300 cursor-pointer"
              style={{ color: "#E60023" }}
            />

            <FaYoutube
              className="hover:scale-125 transition-all duration-300 cursor-pointer"
              style={{ color: "#FF0000" }}
            />

          </div>

          

      {/* 3D Phone Preview */}

<div className="mt-16 flex justify-center relative">

  {/* Floating Card 1 */}
  <div className="absolute top-10 left-10 bg-white rounded-2xl shadow-xl px-4 py-3 hidden md:block">
    <p className="text-xs text-gray-500">Scheduled</p>
    <p className="font-bold">24 Posts</p>
  </div>

  {/* Floating Card 2 */}
  <div className="absolute top-24 right-10 bg-white rounded-2xl shadow-xl px-4 py-3 hidden md:block">
    <p className="text-xs text-gray-500">Engagement</p>
    <p className="font-bold text-green-500">+38%</p>
  </div>

  {/* Floating Card 3 */}
  <div className="absolute bottom-10 left-12 bg-white rounded-2xl shadow-xl px-4 py-3 hidden md:block">
    <p className="text-xs text-gray-500">Followers</p>
    <p className="font-bold">12.4K</p>
  </div>

  <Image
    src="/images/3d-phone.png"
    alt="SocialPilot Mobile App"
    width={450}
    height={450}
    className="drop-shadow-2xl hover:scale-105 transition-all duration-500"
  />

</div>

        </div>

      </section>

      
            {/* ================= Statistics ================= */}

     {/* ================= Statistics ================= */}

<section className="max-w-6xl mx-auto px-6 -mt-6 mb-24">

  <div className="grid grid-cols-2 md:grid-cols-4 gap-6">

    {[
      ["100K+", "Posts Scheduled"],
      ["15K+", "Happy Users"],
      ["99.9%", "Uptime"],
      ["24/7", "Support"],
    ].map(([value, label]) => (

      <div
        key={label}
        className="rounded-3xl p-7 text-center transition-all duration-300 hover:-translate-y-3 hover:shadow-2xl"
        style={{
          background: "#FFFFFF",
          border: "1px solid #D6ECFF",
        }}
      >

        <h2
          className="text-4xl font-extrabold"
          style={{ color: COLORS.primary }}
        >
          {value}
        </h2>

        <p
          className="mt-3"
          style={{ color: COLORS.body }}
        >
          {label}
        </p>

      </div>

    ))}

  </div>

</section>

{/* ================= FEATURES ================= */}

<section className="max-w-7xl mx-auto px-6 pb-28">

  <h2
    className="text-5xl font-bold text-center mb-5"
    style={{ color: COLORS.text }}
  >
    Everything you need
  </h2>

  <p
    className="text-center text-lg mb-16 max-w-3xl mx-auto"
    style={{ color: COLORS.body }}
  >
    Powerful tools to schedule, manage and grow your social presence
    from one beautiful dashboard.
  </p>

  <div className="grid md:grid-cols-3 gap-8">

    {/* Card 1 */}

    <div
      className="rounded-3xl p-8 transition-all duration-300 hover:-translate-y-3 hover:shadow-2xl"
      style={{
        background: "#FFFFFF",
        border: "1px solid #D6ECFF",
      }}
    >

      <FaCalendarAlt
        size={48}
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
        Publish content automatically across all major social media
        platforms without switching between apps.
      </p>

    </div>

    {/* Card 2 */}

    <div
      className="rounded-3xl p-8 transition-all duration-300 hover:-translate-y-3 hover:shadow-2xl"
      style={{
        background: "#FFFFFF",
        border: "1px solid #D6ECFF",
      }}
    >

      <FaChartLine
        size={48}
        style={{ color: COLORS.primary }}
      />

      <h3
        className="text-2xl font-bold mt-6 mb-4"
        style={{ color: COLORS.primary }}
      >
        Smart Analytics
      </h3>

      <p
        className="leading-8"
        style={{ color: COLORS.body }}
      >
        Understand audience engagement, impressions and campaign
        performance using beautiful visual reports.
      </p>

    </div>

    {/* Card 3 */}

    <div
      className="rounded-3xl p-8 transition-all duration-300 hover:-translate-y-3 hover:shadow-2xl"
      style={{
        background: "#FFFFFF",
        border: "1px solid #D6ECFF",
      }}
    >

      <FaUsers
        size={48}
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
        Invite team members, assign roles and collaborate together
        without leaving the platform.
      </p>

    </div>

  </div>

</section>

{/* ================= CALL TO ACTION ================= */}
            
{/* ================= CALL TO ACTION ================= */}

<section className="py-24 px-6">

  <div
    className="max-w-6xl mx-auto rounded-[40px] p-14 text-center"
    style={{
      background: "#FFFFFF",
      border: "1px solid #D6ECFF",
      boxShadow: "0 25px 60px rgba(37,99,235,0.10)",
    }}
  >

    <div className="text-6xl mb-6">
      🚀
    </div>

    <h2
      className="text-5xl font-bold mb-6"
      style={{
        color: COLORS.text,
      }}
    >
      Ready to Grow Your Brand?
    </h2>

    <p
      className="text-lg leading-8 max-w-3xl mx-auto"
      style={{
        color: COLORS.body,
      }}
    >
      Schedule smarter, publish faster and monitor your social media
      performance from one beautiful platform.
    </p>

    <div className="flex justify-center gap-5 mt-10 flex-wrap">

      <Link
        href="/register"
        className="px-8 py-4 rounded-xl text-white font-semibold transition-all duration-300 hover:scale-105 hover:-translate-y-1"
        style={{
          background:
            "linear-gradient(135deg,#0096C7,#0077B6)",
        }}
      >
        Get Started Free
      </Link>

      <Link
        href="/login"
        className="px-8 py-4 rounded-xl font-semibold transition-all duration-300 hover:bg-slate-100"
        style={{
          border: "2px solid #0096C7",
          color: COLORS.primary,
        }}
      >
        Login
      </Link>

    </div>

    {/* Features */}

    <div className="grid md:grid-cols-3 gap-8 mt-14">

      <div>
        <h3
          className="text-3xl font-bold"
          style={{ color: COLORS.primary }}
        >
          ⚡ Fast
        </h3>

        <p
          className="mt-3"
          style={{ color: COLORS.body }}
        >
          Schedule posts in seconds.
        </p>
      </div>

      <div>
        <h3
          className="text-3xl font-bold"
          style={{ color: COLORS.primary }}
        >
          📊 Smart
        </h3>

        <p
          className="mt-3"
          style={{ color: COLORS.body }}
        >
          Powerful analytics and insights.
        </p>
      </div>

      <div>
        <h3
          className="text-3xl font-bold"
          style={{ color: COLORS.primary }}
        >
          👥 Collaborative
        </h3>

        <p
          className="mt-3"
          style={{ color: COLORS.body }}
        >
          Work with your entire team easily.
        </p>
      </div>

    </div>

  </div>

</section>

{/* ================= FOOTER ================= */}
      

     {/* ================= FOOTER ================= */}

<footer
  className="pt-20 pb-10 mt-10"
  style={{
    background: COLORS.sidebar,
  }}
>
  <div className="max-w-7xl mx-auto px-6">

    <div className="grid md:grid-cols-4 gap-10">

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
          Your all-in-one social media management platform.
          Schedule, publish and analyze your content with ease.
        </p>

      </div>

      {/* Product */}

      <div>

        <h3 className="text-xl font-semibold text-white mb-5">
          Product
        </h3>

        <div className="space-y-3">

          <p className="text-slate-300 hover:text-white cursor-pointer">
            Features
          </p>

          <p className="text-slate-300 hover:text-white cursor-pointer">
            Analytics
          </p>

          <p className="text-slate-300 hover:text-white cursor-pointer">
            Scheduling
          </p>

        </div>

      </div>

      {/* Company */}

      <div>

        <h3 className="text-xl font-semibold text-white mb-5">
          Company
        </h3>

        <div className="space-y-3">

          <Link
            href="/"
            className="block text-slate-300 hover:text-white"
          >
            Home
          </Link>

          <Link
            href="/login"
            className="block text-slate-300 hover:text-white"
          >
            Login
          </Link>

          <Link
            href="/register"
            className="block text-slate-300 hover:text-white"
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

        <div className="flex flex-wrap gap-4 text-3xl">

          <FaFacebook
            className="cursor-pointer hover:scale-125 transition"
            style={{ color: "#1877F2" }}
          />

          <FaInstagram
            className="cursor-pointer hover:scale-125 transition"
            style={{ color: "#E1306C" }}
          />

          <FaLinkedin
            className="cursor-pointer hover:scale-125 transition"
            style={{ color: "#0A66C2" }}
          />

          <FaXTwitter
            className="cursor-pointer hover:scale-125 transition"
            style={{ color: "#FFFFFF" }}
          />

          <FaPinterest
            className="cursor-pointer hover:scale-125 transition"
            style={{ color: "#E60023" }}
          />

          <FaYoutube
            className="cursor-pointer hover:scale-125 transition"
            style={{ color: "#FF0000" }}
          />

        </div>

      </div>

    </div>

    <hr className="my-10 border-slate-700" />

    <div className="flex flex-col md:flex-row justify-between items-center gap-4">

      <p
        style={{
          color: "#CBD5E1",
        }}
      >
        © 2026 SocialPilot. All Rights Reserved.
      </p>

      <p
        style={{
          color: "#94A3B8",
        }}
      >
        Built with ❤️ for Creators & Businesses
      </p>

    </div>

  </div>

</footer>

</main>
);
}