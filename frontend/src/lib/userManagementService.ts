import { Role } from "@/types/user";

export interface ManagedUser {
  id: string;
  name: string;
  email: string;
  role: Role;
  organization: string;
  bio: string;
  phone: string;
  status: "active" | "invited";
  assignedClients: number;
}

let users: ManagedUser[] = [
  { id: "u1", name: "Pranjal", email: "pranjal@socialpilot.com", role: "administrator", organization: "SocialPilot", bio: "Workspace administrator.", phone: "+91 98765 43210", status: "active", assignedClients: 0 },
  { id: "u2", name: "Namratha", email: "namratha@socialpilot.com", role: "content_creator", organization: "SocialPilot", bio: "Social content specialist.", phone: "+91 98765 43211", status: "active", assignedClients: 2 },
  { id: "u3", name: "Aditi", email: "aditi@socialpilot.com", role: "marketing_team", organization: "SocialPilot", bio: "Client campaign manager.", phone: "+91 98765 43212", status: "active", assignedClients: 4 },
  { id: "u4", name: "Rohan", email: "rohan@socialpilot.com", role: "business_user", organization: "Northstar Foods", bio: "Business account owner.", phone: "+91 98765 43213", status: "active", assignedClients: 0 },
];

const delay = () => new Promise((resolve) => setTimeout(resolve, 180));

export async function getManagedUsers(): Promise<ManagedUser[]> {
  await delay();
  return [...users];
}

export async function inviteMember(input: Pick<ManagedUser, "name" | "email" | "role" | "organization">): Promise<ManagedUser> {
  await delay();
  const member: ManagedUser = { id: `u${Date.now()}`, ...input, bio: "", phone: "", status: "invited", assignedClients: 0 };
  users = [...users, member];
  return member;
}

export async function updateManagedUser(id: string, patch: Partial<ManagedUser>): Promise<ManagedUser> {
  await delay();
  const current = users.find((user) => user.id === id);
  if (!current) throw new Error("User not found");
  const updated = { ...current, ...patch };
  users = users.map((user) => (user.id === id ? updated : user));
  return updated;
}
