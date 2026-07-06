import { COLORS } from "../../styles/colors";

export default function DashboardPage() {
  return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{ backgroundColor: COLORS.background }}
    >
      <div
        className="p-8 rounded-xl shadow-lg text-center"
        style={{ backgroundColor: COLORS.card }}
      >
        <h1
          className="text-4xl font-bold"
          style={{ color: COLORS.primary }}
        >
          Welcome to SocialPilot 🚀
        </h1>

        <p
          className="mt-4"
          style={{ color: COLORS.text }}
        >
          Dashboard page is under development.
        </p>
      </div>
    </div>
  );
}