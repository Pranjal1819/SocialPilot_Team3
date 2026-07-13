"use client";

import { useState } from "react";
import Link from "next/link";
import {
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";
import AuthLayout from "@/components/AuthLayout";
import Button from "@/components/Button";
import { COLORS } from "@/constants/theme";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [organization, setOrganization] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [roleError, setRoleError] = useState("");

  const validate = () => {
    let valid = true;

    setEmailError("");
    setPasswordError("");
    setRoleError("");

    if (!email) {
      setEmailError("Email is required");
      valid = false;
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(email)
    ) {
      setEmailError("Please enter a valid email");
      valid = false;
    }

    if (!password) {
      setPasswordError("Password is required");
      valid = false;
    } else if (password.length < 8) {
      setPasswordError("Password must be at least 8 characters");
      valid = false;
    }

    if (!role) {
      setRoleError("Please select a role");
      valid = false;
    }

    return valid;
  };

  const handleLogin = () => {
    if (!validate()) return;

    setLoading(true);

    setTimeout(() => {
      setLoading(false);
      alert("Login Successful!");
    }, 2000);
  };

  return (
    <AuthLayout
      title="Welcome Back!"
      subtitle=""
    >
      <div className="space-y-5">

        {/* Email */}
        <div>
          <div className="relative">
            <FaEnvelope
              className="absolute left-4 top-4"
              style={{ color: COLORS.ocean }}
            />

            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg py-3 pl-12 pr-4 border focus:outline-none focus:ring-2"
              style={{
                borderColor: COLORS.accent,
              }}
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
              className="absolute left-4 top-4"
              style={{ color: COLORS.ocean }}
            />

            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg py-3 pl-12 pr-12 border focus:outline-none focus:ring-2"
              style={{
                borderColor: COLORS.accent,
              }}
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-4"
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

        {/* Organization */}
        <div>
          <input
            type="text"
            placeholder="Organization (Optional)"
            value={organization}
            onChange={(e) => setOrganization(e.target.value)}
            className="w-full rounded-lg py-3 px-4 border focus:outline-none focus:ring-2"
            style={{
              borderColor: COLORS.accent,
            }}
          />
        </div>

        {/* Role */}
        <div>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full rounded-lg py-3 px-4 border focus:outline-none focus:ring-2"
            style={{
              borderColor: COLORS.accent,
            }}
          >
            <option value="">Select Role</option>
            <option>Content Creator</option>
            <option>Marketing Team</option>
            <option>Business User</option>
            <option>Administrator</option>
          </select>

          {roleError && (
            <p className="text-red-500 text-sm mt-1">
              {roleError}
            </p>
          )}
        </div>

        <div onClick={handleLogin}>
          <Button
            text="Login"
            loading={loading}
          />
        </div>

        <p
          className="text-center"
          style={{ color: COLORS.text }}
        >
          Don't have an account?{" "}
          <Link
            href="/register"
            className="font-semibold"
            style={{ color: COLORS.ocean }}
          >
            Register
          </Link>
        </p>

      </div>
    </AuthLayout>
  );
}