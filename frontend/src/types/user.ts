export type Role =
  | "content_creator"
  | "marketing_team"
  | "business_user"
  | "administrator";

export const ROLE_LABELS: Record<Role, string> = {
  content_creator: "Content Creator",
  marketing_team: "Marketing Team",
  business_user: "Business User",
  administrator: "Administrator",
};

export interface CurrentUser {
  name: string;
  email: string;
  role: Role;
}

const validRoles: Role[] = [
  "content_creator",
  "marketing_team",
  "business_user",
  "administrator",
];

/**
 * Maps backend role values to frontend roles.
 *
 * Backend may return:
 * - "admin"
 * - "business_user"
 * - "marketing_team"
 * - "content_creator"
 * - "user" (default for newly registered users)
 *
 * Frontend uses:
 * - "administrator"
 * - "business_user"
 * - "marketing_team"
 * - "content_creator"
 */
export function mapBackendRole(backendRole: string): Role {
  // Backend returns "admin", frontend uses "administrator"
  if (backendRole === "admin") {
    return "administrator";
  }

  // Matching role names
  if (validRoles.includes(backendRole as Role)) {
    return backendRole as Role;
  }

  // Default backend role for newly registered users
  if (backendRole === "user") {
    return "content_creator";
  }

  // Safe fallback for unknown roles
  return "content_creator";
}