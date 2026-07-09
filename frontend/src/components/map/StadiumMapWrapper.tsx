"use client";

import dynamic from "next/dynamic";

const StadiumMap = dynamic(() => import("./StadiumMap"), {
  ssr: false,
  loading: () => (
    <div className="h-[500px] w-full rounded-2xl bg-neutral-900 animate-pulse flex items-center justify-center text-neutral-500 shadow-2xl">
      Initializing Map Engine...
    </div>
  ),
});

export default function StadiumMapWrapper() {
  return <StadiumMap />;
}
