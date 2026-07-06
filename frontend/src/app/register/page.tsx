"use client";

import { useState } from "react";
import Link from "next/link";
import { FaEnvelope, FaLock, FaUser, FaEye, FaEyeSlash } from "react-icons/fa";
import AuthLayout from "../../components/AuthLayout";
import Button from "../../components/Button";
import { COLORS } from "../../styles/colors";

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <AuthLayout
      title="Create Account"
      subtitle="Start managing your social media accounts today."
    >
      <div className="space-y-5">

        {/* Full Name */}
        <div className="relative">
          <FaUser className="absolute left-4 top-4 text-gray-400" />
          <input
            type="text"
            placeholder="Full Name"
            className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
        </div>

        {/* Email */}
        <div className="relative">
          <FaEnvelope className="absolute left-4 top-4 text-gray-400" />
          <input
            type="email"
            placeholder="Email Address"
            className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
        </div>

        {/* Password */}
        <div className="relative">
          <FaLock className="absolute left-4 top-4 text-gray-400" />
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />

          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-4 text-gray-500"
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        </div>

        {/* Confirm Password */}
        <div className="relative">
          <FaLock className="absolute left-4 top-4 text-gray-400" />
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Confirm Password"
            className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
        </div>

        <Button
          text="Create Account"
          type="submit"
        />

        <p
          className="text-center"
          style={{ color: COLORS.text }}
        >
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-semibold"
            style={{ color: COLORS.secondary }}
          >
            Login
          </Link>
        </p>

      </div>
    </AuthLayout>
  );
}