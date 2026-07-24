"use client";

import { PageHeader } from "@/components/ui/page-header";
import { UserManagementPanel } from "@/components/users/UserManagementPanel";
import { useCurrentUser } from "@/hooks/useCurrentUser";

export default function UsersPage() {
  const { role } = useCurrentUser();
  if (role !== "administrator") return <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm text-amber-800">You do not have access to user management.</div>;
  return <div className="space-y-7"><PageHeader eyebrow="Administration" title="User management" description="Invite teammates, review workspace access, and see assigned client responsibilities." /><UserManagementPanel /></div>;
}
