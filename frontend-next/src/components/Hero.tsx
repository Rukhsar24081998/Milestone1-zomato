"use client";

import React, { useState } from "react";
import { UserPreferences } from "@/types";

interface HeroProps {
  onSearch: (prefs: UserPreferences) => void;
  isLoading: boolean;
}

export const Hero: React.FC<HeroProps> = ({ onSearch, isLoading }) => {
  const [location,  setLocation]  = useState("");
  const [budget,    setBudget]    = useState("");
  const [cuisine,   setCuisine]   = useState("");
  const [minRating, setMinRating] = useState(4.0);

  const handleSearch = () => {
    const amount = parseInt(budget, 10);
    const budgetBand: "low" | "medium" | "high" =
      !amount || amount <= 500 ? "low" : amount <= 1500 ? "medium" : "high";

    onSearch({
      location:   location.trim() || undefined,
      budget:     budgetBand,
      min_rating: minRating,
      cuisine:    cuisine.trim() || undefined,
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <section className="relative w-full h-[85vh] md:h-[75vh] overflow-hidden flex items-center justify-center">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/45 z-10" />

      {/* Hero image */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1600&auto=format&fit=crop&q=80"
        alt=""
        aria-hidden="true"
        className="absolute inset-0 w-full h-full object-cover"
      />

      {/* Content */}
      <div className="relative z-20 flex flex-col items-center w-full px-4 md:px-12 text-center text-white">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-3 drop-shadow-lg tracking-tight max-w-3xl">
          Discover Your Next Favorite Meal
        </h1>
        <p className="text-sm md:text-lg mb-7 opacity-90 max-w-2xl leading-relaxed">
          Zomato AI's recommendation engine finds the perfect restaurant tailored to
          your mood, location, and budget.
        </p>

        {/* ── Search bar ─────────────────────────────────────── */}
        <div className="w-full max-w-4xl glass-card p-2 md:p-3 rounded-2xl shadow-2xl flex flex-col md:flex-row gap-2 items-stretch">

          {/* Location */}
          <div className="flex-1 flex items-center gap-2 bg-white rounded-xl px-3 border border-[#e4bebc]/30 min-w-0">
            <span className="material-symbols-outlined text-[#8f6f6e] flex-shrink-0" aria-hidden="true">
              location_on
            </span>
            <input
              className="w-full min-w-0 bg-transparent border-none outline-none focus:ring-0 text-[#1b1c1c] text-sm py-3 placeholder:text-[#8f6f6e]"
              placeholder="Mumbai, Delhi, Bangalore…"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              onKeyDown={handleKeyDown}
              aria-label="City"
            />
          </div>

          {/* Budget */}
          <div className="flex-1 flex items-center gap-2 bg-white rounded-xl px-3 border border-[#e4bebc]/30 min-w-0">
            <span className="material-symbols-outlined text-[#8f6f6e] flex-shrink-0" aria-hidden="true">
              payments
            </span>
            <input
              className="w-full min-w-0 bg-transparent border-none outline-none focus:ring-0 text-[#1b1c1c] text-sm py-3 placeholder:text-[#8f6f6e]"
              placeholder="Budget in ₹ (e.g. 800)"
              type="number"
              min="0"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              onKeyDown={handleKeyDown}
              aria-label="Budget in INR"
            />
          </div>

          {/* Cuisine */}
          <div className="flex-1 flex items-center gap-2 bg-white rounded-xl px-3 border border-[#e4bebc]/30 min-w-0">
            <span className="material-symbols-outlined text-[#8f6f6e] flex-shrink-0" aria-hidden="true">
              restaurant
            </span>
            <input
              className="w-full min-w-0 bg-transparent border-none outline-none focus:ring-0 text-[#1b1c1c] text-sm py-3 placeholder:text-[#8f6f6e]"
              placeholder="North Indian, Italian…"
              type="text"
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
              onKeyDown={handleKeyDown}
              aria-label="Cuisine preference"
            />
          </div>

          {/* Min Rating dropdown */}
          <div className="flex items-center gap-2 bg-white rounded-xl px-3 border border-[#e4bebc]/30 min-w-0">
            <span
              className="material-symbols-outlined text-[#F6AD55] flex-shrink-0 text-[20px]"
              style={{ fontVariationSettings: "'FILL' 1" }}
              aria-hidden="true"
            >
              star
            </span>
            <select
              className="bg-transparent border-none outline-none focus:ring-0 text-[#1b1c1c] text-sm py-3 cursor-pointer pr-1"
              value={minRating}
              onChange={(e) => setMinRating(parseFloat(e.target.value))}
              aria-label="Minimum rating"
            >
              <option value={1}>1 & above</option>
              <option value={2}>2 & above</option>
              <option value={3}>3 & above</option>
              <option value={4}>4 & above</option>
              <option value={5}>5 only</option>
            </select>
          </div>

          {/* Submit */}
          <button
            onClick={handleSearch}
            disabled={isLoading}
            className="bg-[#b7122a] text-white text-sm font-semibold px-6 py-3 md:py-0 rounded-xl hover:bg-[#db313f] active:scale-[0.97] transition-all shadow-lg flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <span className="material-symbols-outlined text-[18px]" aria-hidden="true">bolt</span>
            )}
            {isLoading ? "Finding…" : "Find Flavors"}
          </button>
        </div>
      </div>
    </section>
  );
};
