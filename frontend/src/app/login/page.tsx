"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
  FaUserTag,
} from "react-icons/fa";
import AuthLayout from "../../components/AuthLayout";
import Button from "../../components/Button";
import { COLORS } from "../../styles/colors";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
const [roleError, setRoleError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

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
      setEmailError("Please enter a valid email address");
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
  setRoleError("Please select your role");
  valid = false;
}

    return valid;
  };

  const handleLogin = () => {
    if (!validate()) return;

    setLoading(true);

    // Temporary delay to simulate API call
    setTimeout(() => {
      setLoading(false);
      router.push("/dashboard");
    }, 2000);
  };

  return (
    <AuthLayout
      title="Welcome Back!"
      subtitle="Login to continue managing your social media accounts."
    >
      <div className="space-y-5">

        {/* Email */}
        <div>
          <div className="relative">
            <FaEnvelope className="absolute left-4 top-4 text-gray-400" />

            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-600"
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
            <FaLock className="absolute left-4 top-4 text-gray-400" />

            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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

          {passwordError && (
            <p className="text-red-500 text-sm mt-1">
              {passwordError}
            </p>
          )}
        </div>
{/* Role */}
<div>
  <div className="relative">
    <FaUserTag className="absolute left-4 top-4 text-gray-400" />

    <select
      value={role}
      onChange={(e) => setRole(e.target.value)}
      className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-teal-600"
    >
      <option value="">Select Role</option>
      <option value="Content Creator">Content Creator</option>
      <option value="Marketing Team">Marketing Team</option>
      <option value="Business Owner">Business Owner</option>
      <option value="Administrator">Administrator</option>
    </select>
  </div>

  {roleError && (
    <p className="text-red-500 text-sm mt-1">
      {roleError}
    </p>
  )}
</div>
        {/* Login Button */}
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
            style={{ color: COLORS.secondary }}
          >
            Register
          </Link>
        </p>

      </div>
    </AuthLayout>
  );
}