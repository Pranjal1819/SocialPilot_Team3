"use client";

import { useRouter } from "next/navigation";
import {
  FaArrowLeft,
  FaBullhorn,
  FaCalendarAlt,
  FaChartLine,
  FaFlag,
  FaGlobe,
  FaPlus,
  FaTasks,
  FaEdit,
  FaTrash,
  FaRupeeSign,
} from "react-icons/fa";

export default function CampaignDetailsPage() {
  const router = useRouter();

  const campaign = {
    id: 1,
    name: "Nike Summer Sale Campaign",
    objective: "Increase Brand Awareness",
    description:
      "This campaign promotes Nike's new summer collection across Instagram, Facebook and LinkedIn. Multiple scheduled posts are grouped together under one marketing objective.",

    platform: "Instagram, Facebook, LinkedIn",

    category: "Product Launch",

    priority: "High",

    status: "Running",

    budget: "₹2,00,000",

    spent: "₹1,35,000",

    remaining: "₹65,000",

    startDate: "01 Jul 2026",

    endDate: "31 Jul 2026",

    progress: 72,

    totalPosts: 25,

    publishedPosts: 18,
  };

  const posts = [
    "Summer Collection Teaser",
    "Launch Announcement",
    "Customer Testimonial",
    "Limited Time Offer",
  ];

  const timeline = [
    "Campaign Created",
    "Content Planned",
    "Posts Scheduled",
    "Campaign Running",
    "Campaign Ends",
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 p-8">

      <div className="mx-auto max-w-7xl">

        <button
          onClick={() => router.push("/campaign")}
          className="mb-8 flex items-center gap-2 rounded-xl border bg-white px-5 py-3 shadow hover:bg-slate-100"
        >
          <FaArrowLeft />
          Back to Dashboard
        </button>

        <div className="mb-8 flex flex-col justify-between gap-6 lg:flex-row lg:items-center">

          <div className="flex items-center gap-4">

            <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-4 text-white">

              <FaBullhorn className="text-3xl" />

            </div>

            <div>

              <h1 className="text-4xl font-bold text-slate-900">
                {campaign.name}
              </h1>

              <p className="mt-2 text-slate-500">
                Campaign Overview
              </p>

            </div>

          </div>

          <div className="flex gap-3">

            <span className="rounded-full bg-green-100 px-5 py-2 font-semibold text-green-700">
              {campaign.status}
            </span>

            <span className="rounded-full bg-red-100 px-5 py-2 font-semibold text-red-700">
              {campaign.priority} Priority
            </span>

          </div>

        </div>

        <div className="grid gap-8 lg:grid-cols-3">

          <div className="space-y-8 lg:col-span-2">

            <div className="rounded-2xl bg-white p-8 shadow-lg">

              <h2 className="mb-6 text-2xl font-bold">
                Campaign Information
              </h2>

              <div className="grid gap-5 md:grid-cols-2">

                <InfoCard
                  icon={<FaBullhorn className="text-blue-600" />}
                  title="Campaign"
                  value={campaign.name}
                />

                <InfoCard
                  icon={<FaGlobe className="text-cyan-600" />}
                  title="Platforms"
                  value={campaign.platform}
                />

                <InfoCard
                  icon={<FaFlag className="text-red-500" />}
                  title="Category"
                  value={campaign.category}
                />

                <InfoCard
                  icon={<FaChartLine className="text-purple-600" />}
                  title="Objective"
                  value={campaign.objective}
                />

                <InfoCard
                  icon={<FaCalendarAlt className="text-green-600" />}
                  title="Start Date"
                  value={campaign.startDate}
                />

                <InfoCard
                  icon={<FaCalendarAlt className="text-orange-500" />}
                  title="End Date"
                  value={campaign.endDate}
                />

              </div>

              <div className="mt-6 rounded-xl bg-slate-50 p-5">

                <h3 className="mb-2 font-semibold">
                  Description
                </h3>

                <p className="text-slate-600">
                  {campaign.description}
                </p>

              </div>

            </div>
                        {/* Campaign Progress */}

            <div className="rounded-2xl bg-white p-8 shadow-lg">

              <div className="mb-5 flex items-center justify-between">

                <h2 className="text-2xl font-bold text-slate-900">
                  Campaign Progress
                </h2>

                <span className="text-xl font-bold text-blue-600">
                  {campaign.progress}%
                </span>

              </div>


              <p className="mb-5 text-slate-600">
                {campaign.publishedPosts} of {campaign.totalPosts} posts
                published successfully
              </p>


              <div className="h-4 overflow-hidden rounded-full bg-slate-200">

                <div
                  className="h-full rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"
                  style={{
                    width: `${campaign.progress}%`,
                  }}
                />

              </div>

            </div>


            {/* Assigned Posts */}

            <div className="rounded-2xl bg-white p-8 shadow-lg">


              <div className="mb-6 flex items-center justify-between">


                <h2 className="text-2xl font-bold text-slate-900">
                  Assigned Posts
                </h2>


                <button
                  onClick={() =>
                    router.push("/campaign/assign-posts")
                  }
                  className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-5 py-3 font-semibold text-white hover:scale-105 transition"
                >

                  <FaPlus />

                  Assign Posts

                </button>


              </div>



              <div className="space-y-4">


                {posts.map((post, index) => (

                  <div
                    key={index}
                    className="flex items-center justify-between rounded-xl border p-5 hover:bg-blue-50"
                  >


                    <div className="flex items-center gap-4">


                      <div className="rounded-full bg-green-100 p-3">

                        <FaTasks className="text-green-600" />

                      </div>


                      <div>

                        <p className="font-semibold text-slate-800">
                          {post}
                        </p>


                        <p className="text-sm text-slate-500">
                          Scheduled post
                        </p>

                      </div>


                    </div>



                    <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">

                      Scheduled

                    </span>


                  </div>


                ))}


              </div>


            </div>


          </div>
                    {/* Right Sidebar */}

          <div className="space-y-8">


            {/* Budget Summary */}

            <div className="rounded-2xl bg-white p-8 shadow-lg">

              <h2 className="mb-6 text-xl font-bold text-slate-900">
                Budget Summary
              </h2>


              <BudgetCard
                title="Allocated Budget"
                value={campaign.budget}
              />


              <BudgetCard
                title="Spent Budget"
                value={campaign.spent}
              />


              <BudgetCard
                title="Remaining Budget"
                value={campaign.remaining}
              />

            </div>



            {/* Timeline */}

            <div className="rounded-2xl bg-white p-8 shadow-lg">


              <h2 className="mb-6 text-xl font-bold text-slate-900">
                Campaign Timeline
              </h2>


              <div className="space-y-5">


                {timeline.map((item, index) => (

                  <div
                    key={index}
                    className="flex items-center gap-4"
                  >

                    <div className="h-4 w-4 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500">
                    </div>


                    <span className="text-slate-700">
                      {item}
                    </span>


                  </div>

                ))}


              </div>


            </div>



            {/* Quick Actions */}


            <div className="rounded-2xl bg-white p-8 shadow-lg">


              <h2 className="mb-6 text-xl font-bold text-slate-900">
                Quick Actions
              </h2>



              <div className="space-y-4">


                <button
                  onClick={() =>
                    alert("Edit Campaign feature coming soon")
                  }
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 py-3 font-semibold text-white hover:scale-105 transition"
                >

                  <FaEdit />

                  Edit Campaign

                </button>



                <button
                  onClick={() =>
                    router.push("/campaign/assign-posts")
                  }
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-green-600 to-emerald-500 py-3 font-semibold text-white hover:scale-105 transition"
                >

                  <FaPlus />

                  Assign Posts

                </button>




                <button
                  onClick={() => {

                    if (
                      confirm("Are you sure you want to delete this campaign?")
                    ) {

                      router.push("/campaign");

                    }

                  }}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-red-600 to-rose-500 py-3 font-semibold text-white hover:scale-105 transition"
                >

                  <FaTrash />

                  Delete Campaign

                </button>


              </div>


            </div>


          </div>


        </div>
        id="part4"
      </div>

    </main>
  );
}


/* ---------------- Reusable Components ---------------- */


function InfoCard({
  icon,
  title,
  value,
}: {
  icon: React.ReactNode;
  title: string;
  value: string;
}) {

  return (

    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:shadow-md transition">


      <div className="mb-3 flex items-center gap-3">


        <div className="rounded-lg bg-slate-100 p-3">

          {icon}

        </div>


        <p className="text-xs font-semibold uppercase text-slate-500">

          {title}

        </p>


      </div>



      <p className="font-semibold text-slate-800">

        {value}

      </p>



    </div>

  );

}



function BudgetCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {


  return (

    <div className="mb-4 flex items-center justify-between rounded-xl bg-slate-50 p-4">


      <div className="flex items-center gap-3">


        <div className="rounded-lg bg-emerald-100 p-2">

          <FaRupeeSign className="text-emerald-600" />

        </div>



        <span className="font-medium text-slate-700">

          {title}

        </span>


      </div>



      <span className="font-bold text-slate-900">

        {value}

      </span>



    </div>

  );

}