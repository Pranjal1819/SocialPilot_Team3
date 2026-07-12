import Link from "next/link";
import { COLORS } from "../styles/colors";

export default function Home() {
  return (
    <main
      className="min-h-screen"
      style={{ backgroundColor: COLORS.background }}
    >
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-24 text-center">

        <h1
          className="text-6xl md:text-7xl font-bold tracking-tight mb-6"
          style={{ color: COLORS.text }}
        >
          SocialPilot 
        </h1>

        <p
          className="max-w-3xl mx-auto text-lg leading-8 mb-12"
          style={{ color: COLORS.body }}
        >
          Plan, publish and analyze your social media content
          from one unified platform.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-5">

          <Link
            href="/register"
            className="px-8 py-4 rounded-xl text-white font-semibold transition-all duration-300 hover:-translate-y-1"
            style={{
              background:
                "linear-gradient(135deg, #0096C7 0%, #0077B6 100%)",
              boxShadow:
                "0 12px 30px -10px rgba(0,119,182,0.4)",
            }}
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="px-8 py-4 rounded-xl font-semibold border transition-all duration-300 hover:bg-white"
            style={{
              borderColor: COLORS.inputBorder,
              color: COLORS.primary,
              backgroundColor: "#FFFFFF",
            }}
          >
            Login
          </Link>

        </div>

      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 pb-24">

        <h2
          className="text-4xl font-bold tracking-tight text-center mb-14"
          style={{ color: COLORS.text }}
        >
          Why Choose SocialPilot?
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          {/* Card 1 */}
          <div
            className="rounded-3xl p-8 transition-all duration-300 hover:-translate-y-1"
            style={{
              backgroundColor: COLORS.card,
              boxShadow:
                "0 8px 30px -12px rgba(15,23,42,0.12)",
            }}
          >
            <h3
              className="text-2xl font-semibold mb-4"
              style={{ color: COLORS.primary }}
            >
              📅 Schedule Posts
            </h3>

            <p
              className="leading-7"
              style={{ color: COLORS.body }}
            >
              Plan and publish content across multiple
              social media platforms effortlessly.
            </p>
          </div>

          {/* Card 2 */}
          <div
            className="rounded-3xl p-8 transition-all duration-300 hover:-translate-y-1"
            style={{
              backgroundColor: COLORS.card,
              boxShadow:
                "0 8px 30px -12px rgba(15,23,42,0.12)",
            }}
          >
            <h3
              className="text-2xl font-semibold mb-4"
              style={{ color: COLORS.primary }}
            >
              📈 Analytics
            </h3>

            <p
              className="leading-7"
              style={{ color: COLORS.body }}
            >
              Track engagement, audience growth and
              campaign performance with real-time insights.
            </p>
          </div>

          {/* Card 3 */}
          <div
            className="rounded-3xl p-8 transition-all duration-300 hover:-translate-y-1"
            style={{
              backgroundColor: COLORS.card,
              boxShadow:
                "0 8px 30px -12px rgba(15,23,42,0.12)",
            }}
          >
            <h3
              className="text-2xl font-semibold mb-4"
              style={{ color: COLORS.primary }}
            >
              👥 Team Collaboration
            </h3>

            <p
              className="leading-7"
              style={{ color: COLORS.body }}
            >
              Collaborate with creators, marketing teams
              and administrators from one workspace.
            </p>
          </div>

        </div>

      </section>
    </main>
  );
}