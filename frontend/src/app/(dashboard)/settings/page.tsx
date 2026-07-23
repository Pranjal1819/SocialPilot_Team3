import SettingsTabs from "@/components/settings/SettingsTabs";

export default function SettingsPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">
          Manage your profile, account, and team.
        </h1>
      </div>
      <SettingsTabs />
    </div>
  );
}