import {
  FaBullhorn,
  FaPlayCircle,
  FaCheckCircle,
  FaChartLine,
} from "react-icons/fa";

import { mockCampaigns } from "@/lib/mockCampaigns";

export default function CampaignStats() {
  // Dynamic Statistics
  const totalCampaigns = mockCampaigns.length;

  const runningCampaigns = mockCampaigns.filter(
    (campaign) => campaign.status === "Running"
  ).length;

  const completedCampaigns = mockCampaigns.filter(
    (campaign) => campaign.status === "Completed"
  ).length;

  const averageProgress =
    totalCampaigns > 0
      ? Math.round(
          mockCampaigns.reduce(
            (sum, campaign) => sum + campaign.progress,
            0
          ) / totalCampaigns
        )
      : 0;

  const stats = [
    {
      title: "Total Campaigns",
      value: totalCampaigns,
      icon: <FaBullhorn />,
      color: "bg-blue-100 text-blue-600",
    },
    {
      title: "Running",
      value: runningCampaigns,
      icon: <FaPlayCircle />,
      color: "bg-green-100 text-green-600",
    },
    {
      title: "Completed",
      value: completedCampaigns,
      icon: <FaCheckCircle />,
      color: "bg-purple-100 text-purple-600",
    },
    {
      title: "Average Progress",
      value: `${averageProgress}%`,
      icon: <FaChartLine />,
      color: "bg-orange-100 text-orange-600",
    },
  ];

  return (
    <div className="mb-8 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {stats.map((item) => (
        <div
          key={item.title}
          className="rounded-2xl border border-gray-200 bg-white p-6 shadow-md transition duration-300 hover:-translate-y-1 hover:shadow-xl"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">
                {item.title}
              </p>

              <h2 className="mt-2 text-3xl font-bold text-gray-800">
                {item.value}
              </h2>
            </div>

            <div
              className={`rounded-xl p-4 text-2xl ${item.color}`}
            >
              {item.icon}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}