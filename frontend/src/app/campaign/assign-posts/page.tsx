"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/components/DashboardLayout";
import {
  FaTasks,
  FaCheckCircle,
  FaBullhorn,
  FaCalendarAlt,
  FaChartLine,
} from "react-icons/fa";


export default function AssignPostsPage() {
    const router = useRouter();


  const [selectedPosts, setSelectedPosts] = useState<number[]>([]);
  const [selectedCampaign, setSelectedCampaign] = useState(
    "Nike Summer Sale Campaign"
  );

  const [assigned, setAssigned] = useState(false);



  const campaigns = [
    {
      name:"Nike Summer Sale Campaign",
      objective:"Increase Brand Awareness",
      duration:"01 Jul 2026 - 31 Jul 2026",
      progress:"72%"
    },
    {
      name:"Samsung Independence Offer",
      objective:"Product Promotion",
      duration:"01 Aug 2026 - 20 Aug 2026",
      progress:"20%"
    },
    {
      name:"Apple Back to School",
      objective:"Sales Growth",
      duration:"01 Jun 2026 - 30 Jun 2026",
      progress:"100%"
    }
  ];



  const posts = [
    {
      id:1,
      title:"Summer Collection Teaser",
      platform:"Instagram",
      date:"10 July 2026"
    },
    {
      id:2,
      title:"Launch Announcement",
      platform:"Facebook",
      date:"15 July 2026"
    },
    {
      id:3,
      title:"Customer Testimonial",
      platform:"LinkedIn",
      date:"20 July 2026"
    },
    {
      id:4,
      title:"Limited Time Offer",
      platform:"Instagram",
      date:"25 July 2026"
    }
  ];



  const campaignInfo =
    campaigns.find(
      (campaign)=>
        campaign.name === selectedCampaign
    );



  function handleSelect(id:number){

    if(selectedPosts.includes(id)){

      setSelectedPosts(
        selectedPosts.filter(
          postId=>postId!==id
        )
      );

    }
    else{

      setSelectedPosts([
        ...selectedPosts,
        id
      ]);

    }

    setAssigned(false);

  }


function handleAssign(){

  if(selectedPosts.length === 0){

    alert("Please select at least one post");

    return;

  }


  setAssigned(true);


  alert(
    `${selectedPosts.length} posts assigned successfully to ${selectedCampaign}`
  );


  setSelectedPosts([]);


  router.push("/campaign/1");

}







return (
  <DashboardLayout>
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">

      <div className="mx-auto max-w-6xl"></div>

        <div className="mb-8">

          <h1 className="text-4xl font-bold text-slate-900">
            Assign Posts to Campaign
          </h1>

          <div className="mt-2 h-1 w-24 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500"></div>


          <p className="mt-4 text-slate-600">
            Select scheduled posts and associate them with a campaign.
          </p>

        </div>



        {/* Campaign Selection */}

        <div className="mb-8 rounded-2xl bg-white p-6 shadow-lg">


          <label className="mb-3 block font-semibold text-slate-800">
            Select Campaign
          </label>


         <select
  value={selectedCampaign}
  onChange={(e) => {
    setSelectedCampaign(e.target.value);
    setAssigned(false);
  }}
  className="w-full rounded-xl border border-slate-300 bg-white p-3 shadow-sm focus:border-blue-500 focus:outline-none"
>

  {campaigns.map((campaign) => (

    <option
      key={campaign.name}
      value={campaign.name}
    >
      {campaign.name}
    </option>

  ))}

</select>
{campaignInfo && (

  <div className="mt-6 rounded-2xl border border-blue-100 bg-gradient-to-r from-blue-50 to-cyan-50 p-6">

    <div className="flex items-center gap-3">

      <div className="rounded-xl bg-blue-600 p-3 text-white">
        <FaBullhorn />
      </div>

      <div>

        <h3 className="text-xl font-bold text-slate-800">
          {campaignInfo.name}
        </h3>

        <p className="text-slate-600">
          {campaignInfo.objective}
        </p>

      </div>

    </div>

    <div className="mt-5 grid gap-4 md:grid-cols-2">

      <div className="flex items-center gap-2 rounded-xl bg-white p-4 shadow">

        <FaCalendarAlt className="text-blue-600" />

        <div>

          <p className="text-xs text-slate-500">
            Duration
          </p>

          <p className="font-semibold">
            {campaignInfo.duration}
          </p>

        </div>

      </div>

      <div className="flex items-center gap-2 rounded-xl bg-white p-4 shadow">

        <FaChartLine className="text-green-600" />

        <div>

          <p className="text-xs text-slate-500">
            Current Progress
          </p>

          <p className="font-semibold">
            {campaignInfo.progress}
          </p>

        </div>

      </div>

    </div>

  </div>

)}

        </div>





        {/* Posts */}


        <div className="rounded-2xl bg-white p-8 shadow-lg">
            {
assigned && (

<div className="mb-6 flex items-center gap-3 rounded-xl bg-green-50 p-4 text-green-700">

<FaCheckCircle className="text-xl"/>

<p className="font-semibold">
Posts successfully assigned to campaign.
</p>

</div>

)
}


          <h2 className="mb-6 text-2xl font-bold">
            Available Scheduled Posts
          </h2>



       <div className="mb-5 flex items-center justify-between">

  <h2 className="text-2xl font-bold text-slate-900">
    
  </h2>


  <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">

    {selectedPosts.length} Selected

  </span>

</div>



<div className="space-y-4">


{
posts.map((post)=>(


<div
key={post.id}
className={`flex items-center justify-between rounded-xl border p-5 transition

${
selectedPosts.includes(post.id)

?

"border-blue-500 bg-blue-50 shadow-md"

:

"border-slate-200 hover:border-blue-300 hover:bg-slate-50"

}

`}
>


<div className="flex items-center gap-4">


<input

type="checkbox"

checked={
selectedPosts.includes(post.id)
}

onChange={()=>
handleSelect(post.id)
}

className="h-5 w-5 cursor-pointer accent-blue-600"

/>



<div className="rounded-xl bg-blue-100 p-3">

<FaTasks className="text-blue-600 text-xl"/>

</div>



<div>

<h3 className="font-semibold text-slate-800">

{post.title}

</h3>


<p className="text-sm text-slate-500">

{post.platform} • {post.date}

</p>


</div>


</div>



<span className="rounded-full bg-yellow-100 px-4 py-2 text-sm font-semibold text-yellow-700">

Unassigned

</span>



</div>


))
}


</div>



          <button

onClick={handleAssign}

disabled={selectedPosts.length===0}

className={`mt-8 flex items-center gap-2 rounded-xl px-6 py-3 font-semibold text-white transition

${
selectedPosts.length===0

?

"cursor-not-allowed bg-slate-400"

:

"bg-gradient-to-r from-blue-600 to-cyan-500 hover:scale-105"

}

`}

>

            <FaCheckCircle/>

            Assign Selected Posts

          </button>


        </div>


      </div>


    </DashboardLayout>

  );
}