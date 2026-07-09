import Link from "next/link";
import { COLORS } from "../styles/colors";

export default function Home() {
  return (
    <main
      className="min-h-screen"
      style={{ backgroundColor: COLORS.background }}
    >
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center text-center px-6 py-24">

        <h1
          className="text-6xl font-bold mb-6"
          style={{ color: COLORS.primary }}
        >
          SocialPilot 🚀
        </h1>

        <p
          className="max-w-2xl text-lg mb-10"
          style={{ color: COLORS.text }}
        >
          Manage, schedule and analyze all your social media accounts
          from one powerful platform.
        </p>

        <div className="flex gap-5">

          <Link
            href="/register"
            className="px-8 py-4 rounded-lg text-white font-semibold shadow-lg"
            style={{ backgroundColor: COLORS.secondary }}
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="px-8 py-4 rounded-lg font-semibold border-2"
            style={{
              borderColor: COLORS.secondary,
              color: COLORS.secondary,
            }}
          >
            Login
          </Link>

        </div>

      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-6 pb-20">

        <h2
          className="text-4xl font-bold text-center mb-12"
          style={{ color: COLORS.primary }}
        >
          Why Choose SocialPilot?
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          <div
            className="rounded-xl shadow-lg p-8"
            style={{ backgroundColor: COLORS.card }}
          >
            <h3
              className="text-xl font-semibold mb-3"
              style={{ color: COLORS.secondary }}
            >
              📅 Schedule Posts
            </h3>

            <p style={{ color: COLORS.text }}>
              Plan and publish your social media content
              across multiple platforms effortlessly.
            </p>
          </div>

          <div
            className="rounded-xl shadow-lg p-8"
            style={{ backgroundColor: COLORS.card }}
          >
            <h3
              className="text-xl font-semibold mb-3"
              style={{ color: COLORS.secondary }}
            >
              📈 Analytics
            </h3>

            <p style={{ color: COLORS.text }}>
              Track engagement, audience growth and
              campaign performance using real-time insights.
            </p>
          </div>

          <div
            className="rounded-xl shadow-lg p-8"
            style={{ backgroundColor: COLORS.card }}
          >
            <h3
              className="text-xl font-semibold mb-3"
              style={{ color: COLORS.secondary }}
            >
              👥 Team Collaboration
            </h3>

            <p style={{ color: COLORS.text }}>
              Work together with content creators,
              marketing teams and administrators.
            </p>
          </div>

        </div>

      </section>
    </main>
  );
}