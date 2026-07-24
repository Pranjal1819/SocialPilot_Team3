import { ProfileManagement } from "@/components/users/ProfileManagement";
import { PageHeader } from "@/components/ui/page-header";

export default function ProfilePage() {
  return <div className="space-y-7"><PageHeader eyebrow="Personal workspace" title="Profile and account" description="Manage your personal details, workspace preferences, and account security." /><ProfileManagement /></div>;
}
