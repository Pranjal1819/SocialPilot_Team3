"use client";

import Input from "../../components/Input";
import Button from "../../components/Button";
import { COLORS } from "../../styles/colors";

export default function RegisterPage() {
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
          Create Account
        </h1>

        <p
          className="text-center mb-8"
          style={{ color: COLORS.text }}
        >
          Join SocialPilot today
        </p>

        <div className="space-y-5">
          <Input
            type="text"
            placeholder="Full Name"
          />

          <Input
            type="email"
            placeholder="Email Address"
          />

          <Input
            type="password"
            placeholder="Password"
          />

          <Input
            type="password"
            placeholder="Confirm Password"
          />

          <Button
            text="Register"
            type="submit"
          />
        </div>

        <p
          className="text-center mt-6"
          style={{ color: COLORS.text }}
        >
          Already have an account?{" "}
          <a
            href="/login"
            className="font-semibold"
            style={{ color: COLORS.secondary }}
          >
            Login
          </a>
        </p>
      </div>
    </div>
  );
}