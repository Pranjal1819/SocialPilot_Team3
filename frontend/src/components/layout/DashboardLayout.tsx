import Sidebar from "@/components/sidebar/Sidebar";
import Navbar from "@/components/navbar/Navbar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="flex min-h-screen bg-[#F4FBFD]">
      <Sidebar />
      <div className="flex flex-1 flex-col min-w-0">
        <Navbar />
        <main className="flex-1 min-w-0 px-10 pt-12 pb-10 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}