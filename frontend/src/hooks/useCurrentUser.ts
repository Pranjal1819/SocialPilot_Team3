"use client";

import { useAuth } from "@/contexts/AuthContext";
import { CurrentUser } from "@/types/user";

/**
 * Reads the currently logged-in user from AuthContext (real backend session).
 * Falls back to a mock user only if no one is logged in, so the dashboard
 * still renders during development without requiring a live login.
 */
export function useCurrentUser(): CurrentUser {
  const { user } = useAuth();

  if (user) return user;

  return {
    name: "Pranjal",
    email: "pranjal@socialpilot.com",
    role: "administrator",
  };
}