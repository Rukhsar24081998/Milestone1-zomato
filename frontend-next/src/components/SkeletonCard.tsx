"use client";

import React from "react";

export const SkeletonCard = () => (
  <div className="rounded-3xl overflow-hidden shadow-md bg-white flex flex-col">
    <div className="h-52 shimmer" />
    <div className="p-5 space-y-3">
      <div className="h-5 w-3/4 shimmer rounded-lg" />
      <div className="flex gap-2">
        <div className="h-4 w-16 shimmer rounded-full" />
        <div className="h-4 w-20 shimmer rounded-full" />
      </div>
      <div className="h-16 shimmer rounded-xl" />
    </div>
  </div>
);

export const SkeletonLoader = () => (
  <section className="py-8 px-4 md:px-12 bg-[#fbf9f8]">
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Summary blurb skeleton */}
      <div className="bg-white border border-[#e4bebc] rounded-3xl p-8 shadow-md h-28 shimmer" />
      {/* Cards skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[1, 2, 3, 4].map((i) => <SkeletonCard key={i} />)}
      </div>
    </div>
  </section>
);
