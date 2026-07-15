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
          </p>

          <div className="mt-10 flex flex-wrap justify-center gap-5">

            <Link
              href="/register"
              className="px-8 py-4 rounded-xl bg-white font-semibold transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl"
              style={{
                color: COLORS.primary,
              }}
            >
              Create Free Account
            </Link>

            <Link
              href="/login"
              className="px-8 py-4 rounded-xl border-2 border-white text-white font-semibold transition-all duration-300 hover:bg-white hover:text-sky-700"
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

        </div>

      </footer>

    </main>
  );
}