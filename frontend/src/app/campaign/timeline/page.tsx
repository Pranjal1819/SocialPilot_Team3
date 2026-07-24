"use client";

import Link from "next/link";

import {
  FaBullhorn,
  FaCalendarAlt,
  FaCheckCircle,
  FaClock,
  FaFlag,
  FaTasks,
  FaChartLine,
  FaArrowLeft,
} from "react-icons/fa";


export default function CampaignTimelinePage() {


  const timeline = [

    {
      title:"Campaign Created",
      date:"01 July 2026",
      description:
      "Campaign was created with objectives, budget and target platforms.",
      icon:<FaBullhorn />,
      status:"completed"
    },


    {
      title:"Content Planning",
      date:"05 July 2026",
      description:
      "Marketing team planned campaign content strategy.",
      icon:<FaTasks />,
      status:"completed"
    },


    {
      title:"Posts Scheduled",
      date:"10 July 2026",
      description:
      "Multiple social media posts were scheduled under this campaign.",
      icon:<FaCalendarAlt />,
      status:"completed"
    },


    {
      title:"Campaign Running",
      date:"15 July 2026",
      description:
      "Campaign is currently active and posts are being published.",
      icon:<FaCheckCircle />,
      status:"active"
    },


    {
      title:"Campaign Completion",
      date:"31 July 2026",
      description:
      "Campaign will complete after all scheduled activities are finished.",
      icon:<FaFlag />,
      status:"upcoming"
    }

  ];



  return (

    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 p-8">


      <div className="mx-auto max-w-5xl">


        {/* Heading */}

        <div className="mb-10">


          <h1 className="text-4xl font-bold text-slate-900">
            Campaign Timeline
          </h1>


          <div className="mt-2 h-1 w-24 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"></div>


          <p className="mt-4 text-slate-600">
            Track important campaign activities, milestones and progress.
          </p>
          <div className="mt-6 flex gap-4">


<Link
href="/campaign/1"
className="flex items-center gap-2 rounded-xl bg-white px-5 py-3 font-semibold text-slate-700 shadow hover:bg-slate-100"
>

<FaArrowLeft/>

Campaign Details

</Link>



<Link
href="/campaign/analytics"
className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-5 py-3 font-semibold text-white shadow hover:scale-105"
>

<FaChartLine/>

View Analytics

</Link>


</div>


        </div>
{/* Campaign Summary */}

<div className="mb-8 rounded-2xl bg-white p-6 shadow-lg">


<div className="flex flex-col justify-between gap-5 md:flex-row">


<div>

<h2 className="text-2xl font-bold text-slate-900">

Nike Summer Sale Campaign

</h2>


<p className="mt-2 text-slate-600">

Product Launch • Increase Brand Awareness

</p>

</div>



<div className="rounded-xl bg-blue-50 px-6 py-4">


<p className="text-sm text-slate-500">

Current Progress

</p>


<p className="text-3xl font-bold text-blue-600">

72%

</p>


</div>


</div>


<div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-200">


<div

className="h-full rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"

style={{
width:"72%"
}}

/>


</div>


</div>

        {/* Timeline Container */}

        <div className="rounded-2xl bg-white p-8 shadow-lg">


          <div className="relative">


            {/* Vertical Line */}

            <div className="absolute left-6 top-0 h-full w-1 bg-blue-200"></div>


            <div className="space-y-10">

              {
                timeline.map((item,index)=>(


                  <div
                    key={index}
                    className="relative flex gap-6"
                  >


                    {/* Icon */}

                    <div
                      className={`
                      z-10 flex h-12 w-12 items-center justify-center rounded-full text-white shadow

                      ${
                        item.status==="completed"

                        ?

                        "bg-green-500"

                        :

                        item.status==="active"

                        ?

                        "bg-blue-600"

                        :

                        "bg-slate-400"

                      }

                      `}
                    >

                      {item.icon}

                    </div>


                    {/* Content */}


                    <div className="flex-1 rounded-xl border border-slate-200 p-5">


                      <div className="flex items-center justify-between">


                        <h2 className="text-xl font-bold text-slate-800">
                          {item.title}
                        </h2>


                        <span className="flex items-center gap-2 text-sm text-slate-500">

                          <FaClock />

                          {item.date}

                        </span>


                      </div>


                      <p className="mt-3 text-slate-600">

                        {item.description}

                      </p>


                    </div>


                  </div>


                ))
              }


            </div>


          </div>


        </div>


      </div>


    </main>

  );
}