import DashboardHeader from "@/components/dashboard/DashboardHeader";
import DashboardStats from "@/components/dashboard/DashboardStats";
import CampaignCalendar from "@/components/dashboard/CampaignCalendar";

export default function DashboardPage() {
  return (
    <>
      <DashboardHeader />
      <DashboardStats />
      <CampaignCalendar />
    </>
  );
}