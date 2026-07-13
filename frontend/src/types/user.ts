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
 * Backend confirmed it returns exact role strings matching our Role type.
 * New users default to "user" (not yet assigned a real role by an admin) —
 * we map that specific case to "content_creator" as a safe default until
 * an admin assigns their real role via PATCH /api/users/{id}/role.
 */
export function mapBackendRole(backendRole: string): Role {
  if (validRoles.includes(backendRole as Role)) {
    return backendRole as Role;
  }
  // Covers the "user" default for newly registered, not-yet-assigned accounts
  return "content_creator";
}