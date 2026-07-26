import DashboardLayout from "@/components/DashboardLayout";
import CampaignForm from "@/components/campaign/CampaignForm";

export default function CreateCampaignPage() {
  return (
    <DashboardLayout>
      <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 px-6 py-10">
        <CampaignForm />
      </main>
    </DashboardLayout>
  );
}