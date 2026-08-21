"use client";

import { useEffect } from "react";
import QuickActions from "@/components/dashboard/overview/QuickActions";
import AdministratorStats from "@/components/dashboard/overview/AdministratorStats";
import AccountHealthStrip from "@/components/dashboard/overview/AccountHealthStrip";
import UserRoleBreakdown from "@/components/dashboard/overview/UserRoleBreakdown";
import RecentRegistrations from "@/components/dashboard/overview/RecentRegistrations";
import { useAdminUsersStore } from "@/store/useAdminUsersStore";

export default function AdministratorOverview() {
  const fetchUsers = useAdminUsersStore((state) => state.fetchUsers);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return (
    <div className="space-y-6">
      <QuickActions
        actions={[
          { label: "User Management", href: "/administrator/users", icon: "Users", primary: true },
          { label: "Team Management", href: "/administrator/teams", icon: "Building2" },
        ]}
      />

      <AdministratorStats />

      <AccountHealthStrip />

      <div className="grid gap-6 lg:grid-cols-2">
        <UserRoleBreakdown />
        <RecentRegistrations />
      </div>
    </div>
  );
}