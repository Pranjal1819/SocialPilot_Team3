"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import authService from "@/lib/authService";

import {
  FaEnvelope,
  FaLock,
  FaUser,
  FaEye,
  FaEyeSlash,
  FaBuilding,
} from "react-icons/fa";

import AuthLayout from "@/components/AuthLayout";
import Button from "@/components/Button";
import { COLORS } from "@/constants/theme";

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [organization, setOrganization] = useState("");

  const [nameError, setNameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmPasswordError, setConfirmPasswordError] = useState("");

  const [loading, setLoading] = useState(false);

  const router = useRouter();

  const handleRegister = async () => {
    let valid = true;

    setNameError("");
    setEmailError("");
    setPasswordError("");
    setConfirmPasswordError("");

    if (!name.trim()) {
      setNameError("Full Name is required");
      valid = false;
    }

    if (!email.trim()) {
      setEmailError("Email is required");
      valid = false;
    } else if (email !== email.toLowerCase()) {
      setEmailError("Email should not contain uppercase letters");
      valid = false;
    } else if (email.includes(" ")) {
      setEmailError("Email should not contain spaces");
      valid = false;
    } else if (
      !/^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(email)
    ) {
      setEmailError("Enter a valid email address");
      valid = false;
    }

    if (!password) {
      setPasswordError("Password is required");
      valid = false;
    } else if (password.length < 6) {
      setPasswordError("Password must be at least 6 characters");
      valid = false;
    }

    if (!confirmPassword) {
      setConfirmPasswordError("Confirm Password is required");
      valid = false;
    } else if (password !== confirmPassword) {
      setConfirmPasswordError("Passwords do not match");
      valid = false;
    }

    if (!valid) return;

    setLoading(true);

    try {
      await authService.register(name, email, password);

      alert("Registration Successful!");

      router.push("/login");
    } catch (err) {
      alert(
        err instanceof Error
          ? err.message
          : "Registration failed"
      );
    } finally {
      setLoading(false);
    }
  };

return (
  <AuthLayout
    title="Create Account"
    subtitle="Create your account to start your SocialPilot journey."
  >
    <div className="space-y-5">

      {/* Full Name */}
      <div>
        <div className="relative">
          <FaUser
            className="absolute left-4 top-1/2 -translate-y-1/2"
            style={{ color: COLORS.ocean }}
          />

          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-xl border py-3.5 pl-12 pr-4 bg-slate-50 border-slate-200 transition-all duration-200 focus:bg-white focus:border-blue-300 focus:ring-4 focus:ring-blue-50 outline-none"
          />
        </div>

        {nameError && (
          <p className="text-red-500 text-sm mt-1">
            {nameError}
          </p>
        )}
      </div>

      {/* Email */}
      <div>
        <div className="relative">
          <FaEnvelope
            className="absolute left-4 top-1/2 -translate-y-1/2"
            style={{ color: COLORS.ocean }}
          />

          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-xl border py-3.5 pl-12 pr-4 bg-slate-50 border-slate-200 transition-all duration-200 focus:bg-white focus:border-blue-300 focus:ring-4 focus:ring-blue-50 outline-none"
          />
        </div>

        {emailError && (
          <p className="text-red-500 text-sm mt-1">
            {emailError}
          </p>
        )}
      </div>

      {/* Password */}
      <div>
        <div className="relative">
          <FaLock
            className="absolute left-4 top-1/2 -translate-y-1/2"
            style={{ color: COLORS.ocean }}
          />

          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-xl border py-3.5 pl-12 pr-12 bg-slate-50 border-slate-200 transition-all duration-200 focus:bg-white focus:border-blue-300 focus:ring-4 focus:ring-blue-50 outline-none"
          />

          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-1/2 -translate-y-1/2"
            style={{ color: COLORS.ocean }}
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        </div>

        {passwordError && (
          <p className="text-red-500 text-sm mt-1">
            {passwordError}
          </p>
        )}
      </div>

      {/* Confirm Password */}
      <div>
        <div className="relative">
          <FaLock
            className="absolute left-4 top-1/2 -translate-y-1/2"
            style={{ color: COLORS.ocean }}
          />

          <input
            type={showPassword ? "text" : "password"}
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full rounded-xl border py-3.5 pl-12 pr-4 bg-slate-50 border-slate-200 transition-all duration-200 focus:bg-white focus:border-blue-300 focus:ring-4 focus:ring-blue-50 outline-none"
          />
        </div>

        {confirmPasswordError && (
          <p className="text-red-500 text-sm mt-1">
            {confirmPasswordError}
          </p>
        )}
      </div>

      {/* Organization */}
      <div className="relative">
        <FaBuilding
          className="absolute left-4 top-1/2 -translate-y-1/2"
          style={{ color: COLORS.ocean }}
        />

        <input
          type="text"
          placeholder="Organization (Optional)"
          value={organization}
          onChange={(e) => setOrganization(e.target.value)}
          className="w-full rounded-xl border py-3.5 pl-12 pr-4 bg-slate-50 border-slate-200 transition-all duration-200 focus:bg-white focus:border-blue-300 focus:ring-4 focus:ring-blue-50 outline-none"
        />
      </div>

      <div onClick={handleRegister}>
        <Button
          text="Create Account"
          loading={loading}
        />
      </div>

      <p
        className="text-center"
        style={{ color: COLORS.body }}
      >
        Already have an account?{" "}
        <Link
          href="/login"
          className="font-semibold hover:underline"
          style={{ color: COLORS.primary }}
        >
          Login
        </Link>
      </p>

    </div>
  </AuthLayout>
);
}