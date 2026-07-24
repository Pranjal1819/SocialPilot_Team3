import DashboardHeader from "@/components/dashboard/DashboardHeader";
import DashboardStats from "@/components/dashboard/DashboardStats";
import CampaignCalendar from "@/components/dashboard/CampaignCalendar";

export default function DashboardPage() {
  return (
    <div className="space-y-7 lg:space-y-8">
      <DashboardHeader />
      <DashboardStats />
      <CampaignCalendar />
    </div>
  );
}
