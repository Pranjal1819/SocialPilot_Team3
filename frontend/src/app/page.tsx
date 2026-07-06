import Link from "next/link";
import { COLORS } from "../styles/colors";

export default function Home() {
  return (
    <main
      className="min-h-screen flex items-center justify-center px-6"
      style={{ backgroundColor: COLORS.background }}
    >
      <div
        className="max-w-lg w-full rounded-2xl shadow-xl p-10 text-center"
        style={{ backgroundColor: COLORS.card }}
      >
        <h1
          className="text-5xl font-bold mb-4"
          style={{ color: COLORS.primary }}
        >
          Welcome to SocialPilot 🚀
        </h1>

        <p
          className="text-lg mb-8"
          style={{ color: COLORS.text }}
        >
          Manage your social media accounts efficiently with our platform.
        </p>

        <div className="flex justify-center gap-4">
          <Link
            href="/login"
            className="px-6 py-3 rounded-lg text-white font-semibold transition"
            style={{ backgroundColor: COLORS.secondary }}
          >
            Login
          </Link>

          <Link
            href="/register"
            className="px-6 py-3 rounded-lg font-semibold border transition"
            style={{
              borderColor: COLORS.secondary,
              color: COLORS.secondary,
            }}
          >
            Register
          </Link>
        </div>
      </div>
    </main>
  );
}