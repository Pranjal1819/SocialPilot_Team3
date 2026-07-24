import SettingsTabs from "@/components/settings/SettingsTabs";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-7">
      <div>
        <p className="text-sm font-medium text-cyan-600">Workspace preferences</p>
        <h1 className="mt-1 text-4xl font-bold tracking-tight text-slate-900">Settings</h1>
        <p className="mt-3 text-sm leading-6 text-gray-600">Manage your profile, account, and team preferences.</p>
      </div>
      <SettingsTabs />
    </div>
  );
}
