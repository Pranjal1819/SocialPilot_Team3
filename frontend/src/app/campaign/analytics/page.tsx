"use client";

import Link from "next/link";

import {
  FaArrowLeft,
  FaCheckCircle,
  FaClock,
  FaTasks,
  FaUsers,
  FaBullhorn,
  FaInstagram,
  FaFacebook,
  FaLinkedin,
} from "react-icons/fa";

export default function CampaignAnalyticsPage() {


  const analyticsCards = [

    {
      title:"Total Scheduled Posts",
      value:"25",
      icon:<FaTasks />,
    },

    {
      title:"Published Posts",
      value:"18",
      icon:<FaCheckCircle />,
    },

    {
      title:"Pending Posts",
      value:"7",
      icon:<FaClock />,
    },

    {
      title:"Estimated Reach",
      value:"50K",
      icon:<FaUsers />,
    }

  ];

const platformStats = [
  {
    platform: "Instagram",
    icon: <FaInstagram className="text-pink-500" />,
    posts: 12,
    reach: "25K",
  },
  {
    platform: "Facebook",
    icon: <FaFacebook className="text-blue-600" />,
    posts: 8,
    reach: "15K",
  },
  {
    platform: "LinkedIn",
    icon: <FaLinkedin className="text-sky-700" />,
    posts: 5,
    reach: "10K",
  },
];

const campaignProgress = 72;

  return (

    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 p-8">


      <div className="mx-auto max-w-6xl">


        {/* Header */}

        <div className="mb-10">


          <h1 className="text-4xl font-bold text-slate-900">
            Campaign Analytics Overview
          </h1>


          <div className="mt-2 h-1 w-24 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"></div>


          <p className="mt-4 text-slate-600">
            Monitor campaign performance and publishing progress.
          </p>



          <div className="mt-6">

            <Link
              href="/campaign/timeline"
              className="flex w-fit items-center gap-2 rounded-xl bg-white px-5 py-3 font-semibold text-slate-700 shadow hover:bg-slate-100"
            >

              <FaArrowLeft />

              Back to Timeline

            </Link>


          </div>


        </div>



        {/* Analytics Cards */}

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">


          {
            analyticsCards.map((card,index)=>(


              <div
                key={index}
                className="rounded-2xl bg-white p-6 shadow-lg transition hover:scale-105"
              >


                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-xl text-blue-600">

                  {card.icon}

                </div>



                <h2 className="text-sm font-semibold text-slate-500">

                  {card.title}

                </h2>



                <p className="mt-2 text-3xl font-bold text-slate-900">

                  {card.value}

                </p>



              </div>


            ))
          }


        </div>
        {/* Campaign Progress */}

<div className="mt-10 rounded-2xl bg-white p-8 shadow-lg">

  <div className="mb-6 flex items-center justify-between">

    <h2 className="flex items-center gap-3 text-2xl font-bold text-slate-900">

      <FaBullhorn className="text-blue-600" />

      Campaign Completion

    </h2>

    <span className="text-2xl font-bold text-blue-600">

      {campaignProgress}%

    </span>

  </div>

  <div className="h-5 overflow-hidden rounded-full bg-slate-200">

    <div
      className="h-full rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"
      style={{ width: `${campaignProgress}%` }}
    />

  </div>

  <p className="mt-4 text-slate-600">

    18 out of 25 scheduled posts have been published successfully.

  </p>

</div>
{/* Platform Performance */}

<div className="mt-10">

  <h2 className="mb-6 text-2xl font-bold text-slate-900">
    Platform Performance
  </h2>

  <div className="grid gap-6 md:grid-cols-3">

    {platformStats.map((platform, index) => (

      <div
        key={index}
        className="rounded-2xl bg-white p-6 shadow-lg transition hover:-translate-y-1 hover:shadow-xl"
      >

        <div className="mb-4 flex items-center gap-3">

          <div className="rounded-xl bg-slate-100 p-3">

            {platform.icon}

          </div>

          <h3 className="text-xl font-bold text-slate-800">
            {platform.platform}
          </h3>

        </div>

        <div className="space-y-3">

          <div className="flex justify-between">

            <span className="text-slate-500">
              Published Posts
            </span>

            <span className="font-semibold">
              {platform.posts}
            </span>

          </div>

          <div className="flex justify-between">

            <span className="text-slate-500">
              Estimated Reach
            </span>

            <span className="font-semibold text-emerald-600">
              {platform.reach}
            </span>

          </div>

        </div>

      </div>

    ))}

  </div>

</div>
{/* Campaign Summary */}

<div className="mt-10 grid gap-6 lg:grid-cols-2">

  {/* Campaign Health */}

  <div className="rounded-2xl bg-white p-8 shadow-lg">

    <h2 className="mb-6 text-2xl font-bold text-slate-900">
      Campaign Health
    </h2>

    <div className="space-y-5">

      <div className="flex items-center justify-between">

        <span className="text-slate-600">
          Campaign Status
        </span>

        <span className="rounded-full bg-green-100 px-4 py-2 font-semibold text-green-700">
          Running
        </span>

      </div>

      <div className="flex items-center justify-between">

        <span className="text-slate-600">
          Completion
        </span>

        <span className="font-bold text-blue-600">
          72%
        </span>

      </div>

      <div className="flex items-center justify-between">

        <span className="text-slate-600">
          Total Reach
        </span>

        <span className="font-bold text-emerald-600">
          50,000+
        </span>

      </div>

      <div className="flex items-center justify-between">

        <span className="text-slate-600">
          Engagement
        </span>

        <span className="font-bold text-purple-600">
          Good
        </span>

      </div>

    </div>

  </div>

  {/* Performance Insights */}

  <div className="rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 p-8 text-white shadow-lg">

    <h2 className="mb-6 text-2xl font-bold">
      Performance Insights
    </h2>

    <ul className="space-y-4">

      <li>
        ✅ 18 posts have already been published successfully.
      </li>

      <li>
        📅 7 scheduled posts are waiting for publishing.
      </li>

      <li>
        📈 Estimated audience reach has crossed 50K users.
      </li>

      <li>
        🚀 Campaign is progressing according to schedule.
      </li>

      <li>
        🎯 No scheduling conflicts detected.
      </li>

    </ul>

  </div>

</div>

      </div>


    </main>

  );

} 