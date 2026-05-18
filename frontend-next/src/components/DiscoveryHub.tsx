"use client";

import React, { useState } from "react";
import { UserPreferences, BudgetBand } from "@/types";
import { motion } from "framer-motion";

interface DiscoveryHubProps {
  onSearch: (prefs: UserPreferences) => void;
  isLoading: boolean;
}

export const DiscoveryHub = ({ onSearch, isLoading }: DiscoveryHubProps) => {
  const [prefs, setPrefs] = useState<UserPreferences>({
    location: "",
    cuisine: "",
    budget: "medium",
    min_rating: 4.0,
    notes: "",
  });

  const budgetMap: Record<BudgetBand, string> = {
    low: "Budget ($)",
    medium: "Mid-range ($$)",
    high: "Fine Dining ($$$)",
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(prefs);
  };

  return (
    <section
      id="discover"
      className="relative w-full min-h-[85vh] md:min-h-[75vh] overflow-hidden flex items-center justify-center"
    >
      {/* Hero Background */}
      <div className="absolute inset-0 bg-black/50 z-10" />
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        alt="Flavor Discovery Hero"
        className="absolute inset-0 w-full h-full object-cover"
        src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1600&auto=format&fit=crop&q=80"
      />

      {/* Content */}
      <div className="relative z-20 flex flex-col items-center justify-center w-full px-4 text-center text-white max-w-4xl mx-auto py-20">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl md:text-5xl font-black mb-4 drop-shadow-lg leading-tight"
        >
          Discover Your Next Favorite Meal
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-base md:text-lg font-medium mb-8 opacity-90 max-w-2xl"
        >
          Zomato AI's recommendation engine learns your unique palate to recommend the perfect restaurant, tailored to your mood and location.
        </motion.p>

        {/* Search Form */}
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          onSubmit={handleSubmit}
          className="w-full max-w-3xl glass-card p-2 md:p-3 rounded-2xl shadow-2xl flex flex-col md:flex-row gap-2 items-stretch"
        >
          {/* Location */}
          <div className="flex-1 flex items-center bg-white rounded-xl px-3 border border-[#e4bebc]/50">
            <span className="material-symbols-outlined text-[#8f6f6e] text-xl mr-2">location_on</span>
            <input
              id="location-input"
              type="text"
              placeholder="City e.g. Bangalore"
              className="w-full bg-transparent border-none outline-none text-[#1b1c1c] font-semibold text-sm py-3"
              value={prefs.location}
              onChange={(e) => setPrefs({ ...prefs, location: e.target.value })}
            />
          </div>

          {/* Budget */}
          <div className="flex-1 flex items-center bg-white rounded-xl px-3 border border-[#e4bebc]/50">
            <span className="material-symbols-outlined text-[#8f6f6e] text-xl mr-2">payments</span>
            <select
              id="budget-select"
              className="w-full bg-transparent border-none outline-none text-[#1b1c1c] font-semibold text-sm py-3 cursor-pointer"
              value={prefs.budget}
              onChange={(e) => setPrefs({ ...prefs, budget: e.target.value as BudgetBand })}
            >
              {(Object.entries(budgetMap) as [BudgetBand, string][]).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          {/* Cuisine */}
          <div className="flex-1 flex items-center bg-white rounded-xl px-3 border border-[#e4bebc]/50">
            <span className="material-symbols-outlined text-[#8f6f6e] text-xl mr-2">restaurant</span>
            <input
              id="cuisine-input"
              type="text"
              placeholder="North Indian, Italian..."
              className="w-full bg-transparent border-none outline-none text-[#1b1c1c] font-semibold text-sm py-3"
              value={prefs.cuisine}
              onChange={(e) => setPrefs({ ...prefs, cuisine: e.target.value })}
            />
          </div>

          {/* Submit */}
          <button
            id="find-flavors-btn"
            type="submit"
            disabled={isLoading}
            className="bg-[#b7122a] text-white font-bold px-8 py-3 md:py-0 rounded-xl hover:bg-[#db313f] transition-colors shadow-lg flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <span className="material-symbols-outlined text-sm">bolt</span>
                Find Flavors
              </>
            )}
          </button>
        </motion.form>

        {/* Min Rating Hint */}
        <div className="mt-4 flex items-center gap-4 flex-wrap justify-center">
          <div className="flex items-center gap-2 bg-white/10 rounded-full px-4 py-1.5">
            <span className="text-xs text-white/80 font-medium">Min Rating</span>
            <input
              type="range" min="0" max="5" step="0.5"
              className="w-20 h-1 accent-[#b7122a] cursor-pointer"
              value={prefs.min_rating}
              onChange={(e) => setPrefs({ ...prefs, min_rating: parseFloat(e.target.value) })}
            />
            <span className="text-xs font-bold text-[#F6AD55]">★ {prefs.min_rating?.toFixed(1)}</span>
          </div>
          <div className="flex items-center gap-2 bg-white/10 rounded-full px-4 py-1.5">
            <span className="material-symbols-outlined text-sm text-white/80">tips_and_updates</span>
            <input
              type="text"
              placeholder="Special requests (rooftop, date night...)"
              className="bg-transparent border-none outline-none text-xs text-white placeholder:text-white/50 w-48"
              value={prefs.notes}
              onChange={(e) => setPrefs({ ...prefs, notes: e.target.value })}
            />
          </div>
        </div>
      </div>
    </section>
  );
};
