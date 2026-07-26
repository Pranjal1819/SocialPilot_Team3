import ProgressBar from "./ProgressBar";
import { Campaign } from "@/types/campaign";
import Link from "next/link";
import {
  FaRupeeSign,
  FaCalendarAlt,
  FaClipboardList,
  FaEye,
  FaEdit,
} from "react-icons/fa";

interface CampaignCardProps {
  campaign: Campaign;
}

export default function CampaignCard({ campaign }: CampaignCardProps) {
  const statusColors = {
    Active: "bg-green-100 text-green-700",
    Completed: "bg-purple-100 text-purple-700",
    Draft: "bg-yellow-100 text-yellow-700",
    Planned: "bg-sky-100 text-sky-700",
  };

  const badgeClass =
    statusColors[campaign.status as keyof typeof statusColors] ??
    "bg-gray-100 text-gray-700";

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-md transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">

      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-gray-800">
          {campaign.name}
        </h2>

        <span
          className={`rounded-full px-3 py-1 text-sm font-semibold ${badgeClass}`}
        >
          {campaign.status}
        </span>
      </div>

      {/* Objective */}
      <p className="mt-3 text-sm leading-6 text-gray-600">
        {campaign.objective}
      </p>

      {/* Information Cards */}
      <div className="mt-6 space-y-3">

        {/* Budget */}
        <div className="flex items-center justify-between rounded-xl bg-emerald-50 px-4 py-3">

          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-emerald-100 p-2">
              <FaRupeeSign className="text-emerald-600" />
            </div>

            <span className="font-medium text-gray-700">
              Budget
            </span>
          </div>

          <span className="font-semibold text-emerald-700">
            ₹{campaign.budget.toLocaleString()}
          </span>

        </div>

        {/* Duration */}
        <div className="flex items-center justify-between rounded-xl bg-amber-50 px-4 py-3">

          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-amber-100 p-2">
              <FaCalendarAlt className="text-amber-600" />
            </div>

            <span className="font-medium text-gray-700">
              Duration
            </span>
          </div>

          <span className="text-sm text-gray-700">
            {campaign.startDate} - {campaign.endDate}
          </span>

        </div>

        {/* Posts */}
        <div className="flex items-center justify-between rounded-xl bg-violet-50 px-4 py-3">

          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-violet-100 p-2">
              <FaClipboardList className="text-violet-600" />
            </div>

            <span className="font-medium text-gray-700">
              Posts
            </span>
          </div>

          <span className="font-semibold text-violet-700">
            {campaign.completedPosts}/{campaign.totalPosts}
          </span>

        </div>

      </div>

      {/* Progress */}
      <ProgressBar value={campaign.progress} />

      {/* Buttons */}
   <div className="mt-6 flex gap-3">

<Link
  href={`/campaign/${campaign.id}`}
  className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-4 py-3 font-medium text-white hover:shadow-lg"
>
  <FaEye />
  View Details
</Link>
<Link
  href={`/campaign/${campaign.id}/edit`}
  onClick={() => console.log(`/campaign/${campaign.id}/edit`)}
  className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-gray-100 px-4 py-3 font-medium text-gray-700 hover:bg-gray-200"
>
  <FaEdit />
  Edit
</Link>
</div>

    </div>
  );
}