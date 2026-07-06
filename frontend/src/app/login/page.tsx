"use client";

import Input from "../../components/Input";
import Button from "../../components/Button";
import { COLORS } from "../../styles/colors";

export default function LoginPage() {
  return (
    <div
      className="min-h-screen flex items-center justify-center p-6"
      style={{ backgroundColor: COLORS.background }}
    >
      <div
        className="w-full max-w-md rounded-2xl shadow-xl p-8"
        style={{ backgroundColor: COLORS.card }}
      >
        <h1
          className="text-3xl font-bold text-center mb-2"
          style={{ color: COLORS.primary }}
        >
          SocialPilot
        </h1>

        <p
          className="text-center mb-8"
          style={{ color: COLORS.text }}
        >
          Login to your account
        </p>

        <div className="space-y-5">
          <Input
            type="email"
            placeholder="Enter your email"
          />

          <Input
            type="password"
            placeholder="Enter your password"
          />

          <Button
            text="Login"
            type="submit"
          />
        </div>

        <p
          className="text-center mt-6"
          style={{ color: COLORS.text }}
        >
          Don't have an account?{" "}
          <a
            href="/register"
            className="font-semibold"
            style={{ color: COLORS.secondary }}
          >
            Register
          </a>
        </p>
      </div>
    </div>
  );
}