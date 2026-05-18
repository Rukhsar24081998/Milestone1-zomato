"use client";

import React from "react";
import { PresentationResponse } from "@/types";
import { RestaurantCard } from "./RestaurantCard";
import { motion } from "framer-motion";

interface RecommendationListProps {
  data: PresentationResponse;
}

export const RecommendationList = ({ data }: RecommendationListProps) => {
  if (data.results.length === 0) {
    return (
      <div className="text-center py-20 px-4">
        <span className="material-symbols-outlined text-6xl text-[#e4bebc] block mb-4">
          sentiment_dissatisfied
        </span>
        <p className="text-[#5b403f] text-lg font-semibold">No restaurants found.</p>
        <p className="text-[#8f6f6e] text-sm mt-2">Try adjusting your filters or location.</p>
      </div>
    );
  }

  return (
    <section className="py-8 px-4 md:px-12 bg-[#fbf9f8]">
      <div className="max-w-6xl mx-auto space-y-10">

        {/* AI Summary Blurb */}
        {data.summary_blurb && (
          <motion.div
            initial={{ opacity: 0, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white border border-[#e4bebc] rounded-3xl p-6 md:p-8 shadow-md relative overflow-hidden"
          >
            {/* Decorative accent */}
            <div className="absolute top-0 left-0 w-1.5 h-full bg-[#b7122a] rounded-l-3xl" />
            <div className="pl-4 flex flex-col md:flex-row items-start md:items-center gap-4">
              <div className="w-12 h-12 bg-[#b7122a]/10 rounded-2xl flex items-center justify-center flex-shrink-0">
                <span
                  className="material-symbols-outlined text-[#b7122a] text-2xl"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  auto_awesome
                </span>
              </div>
              <div>
                <p className="text-[10px] font-bold text-[#b7122a] uppercase tracking-[0.2em] mb-1">
                  Zomato AI · Expert Analysis
                </p>
                <p className="text-lg md:text-xl font-bold text-[#1b1c1c] leading-snug">
                  {data.summary_blurb}
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Section Header */}
        <div className="flex justify-between items-end">
          <div>
            <span className="text-[#b7122a] text-xs font-bold uppercase tracking-widest mb-1 block">
              Curated for you
            </span>
            <h2 className="text-2xl font-bold text-[#1b1c1c]">
              {data.results.length} Top Picks
            </h2>
          </div>
          <span className="text-xs text-[#8f6f6e] font-medium bg-[#efeded] px-3 py-1.5 rounded-full">
            Ranked by AI
          </span>
        </div>

        {/* Results Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          {data.results.map((res, i) => (
            <RestaurantCard key={i} restaurant={res} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
};
