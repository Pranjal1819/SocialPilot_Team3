"use client";

import { CurrentUser } from "@/types/user";

/**
 * Temporary mock user until the User Management module (auth/login) is wired up.
 * Replace the return value below once real session data exists. Every component
 * that needs the current user's name/role reads from this one hook — so the
 * real-auth swap is a single-file change.
 */
export function useCurrentUser(): CurrentUser {
  return {
    name: "Pranjal",
    role: "administrator",
  };
}