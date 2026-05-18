"use client";

import React from "react";
import { PresentationResult } from "@/types";
import { motion } from "framer-motion";

interface RestaurantCardProps {
  restaurant: PresentationResult;
  index: number;
}

const FOOD_IMAGES = [
  "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80",
  "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&auto=format&fit=crop&q=80",
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&auto=format&fit=crop&q=80",
  "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&auto=format&fit=crop&q=80",
  "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&auto=format&fit=crop&q=80",
  "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&auto=format&fit=crop&q=80",
];

const ratingColor = (rating?: number) => {
  if (!rating) return "bg-[#8f6f6e]";
  if (rating >= 4.0) return "bg-[#48BB78]";
  if (rating >= 3.0) return "bg-[#F6AD55]";
  return "bg-red-500";
};

const costLabel = (cost?: string) => {
  if (!cost) return "₹₹";
  if (cost === "low") return "₹";
  if (cost === "high") return "₹₹₹";
  return "₹₹";
};

export const RestaurantCard = ({ restaurant, index }: RestaurantCardProps) => {
  const imgSrc = FOOD_IMAGES[index % FOOD_IMAGES.length];

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="group relative rounded-3xl overflow-hidden shadow-lg bg-white hover:shadow-xl transition-shadow duration-300 flex flex-col"
    >
      {/* Image — top 55% */}
      <div className="relative h-52 overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={imgSrc}
          alt={restaurant.name}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />

        {/* Badges */}
        <div className="absolute top-3 left-3 flex gap-2">
          <span className="bg-[#48BB78] text-[10px] font-bold text-white px-2 py-0.5 rounded uppercase tracking-wider">
            #{index + 1} Pick
          </span>
          {restaurant.cost === "low" && (
            <span className="bg-[#b7122a] text-[10px] font-bold text-white px-2 py-0.5 rounded uppercase tracking-wider">
              Budget
            </span>
          )}
        </div>

        {/* Rating Badge */}
        {restaurant.rating && (
          <div className={`absolute top-3 right-3 flex items-center gap-1 ${ratingColor(restaurant.rating)} text-white text-xs font-bold px-2 py-1 rounded-lg`}>
            <span className="material-symbols-outlined text-sm text-yellow-300" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
            {restaurant.rating.toFixed(1)}
          </div>
        )}
      </div>

      {/* Content — bottom 45% */}
      <div className="flex flex-col flex-1 p-5">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-bold text-[#1b1c1c] leading-tight group-hover:text-[#b7122a] transition-colors">
            {restaurant.name}
          </h3>
          <span className="text-sm font-bold text-[#5b403f] bg-[#efeded] px-2 py-0.5 rounded-lg ml-2 flex-shrink-0">
            {costLabel(restaurant.cost)}
          </span>
        </div>

        {/* Cuisine Pills */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {restaurant.cuisines.split(",").slice(0, 3).map((c, i) => (
            <span
              key={i}
              className="text-[11px] font-semibold bg-[#e4bebc]/40 text-[#b7122a] px-2.5 py-0.5 rounded-full border border-[#e4bebc]"
            >
              {c.trim()}
            </span>
          ))}
        </div>

        {/* AI Perspective */}
        <div className="mt-auto bg-[#fbf9f8] border border-[#e4bebc]/50 rounded-xl p-3 relative overflow-hidden">
          <div className="flex items-start gap-2">
            <span
              className="material-symbols-outlined text-[#b7122a] text-base flex-shrink-0 mt-0.5"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              auto_awesome
            </span>
            <div>
              <p className="text-[10px] font-bold text-[#b7122a] uppercase tracking-wider mb-1">Zomato AI Pick</p>
              <p className="text-xs text-[#5b403f] leading-relaxed italic">"{restaurant.explanation}"</p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
