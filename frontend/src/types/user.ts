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
  role: Role;
}