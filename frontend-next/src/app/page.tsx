"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { TrendingSection } from "@/components/TrendingSection";
import { CuisineCategories } from "@/components/CuisineCategories";
import { FeatureSection } from "@/components/FeatureSection";
import { RecommendationList } from "@/components/RecommendationList";
import { SkeletonLoader } from "@/components/SkeletonCard";
import { Footer } from "@/components/Footer";
import { MobileNavigation } from "@/components/MobileNavigation";
import { UserPreferences, PresentationResponse, PresentationResult } from "@/types";
import { API_BASE_URL, getRecommendations } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";

/** Clean up numpy-style cuisine strings like "['North Indian' 'Chinese']" → "North Indian, Chinese" */
function cleanCuisines(raw: string): string {
  return raw
    .replace(/^\[|\]$/g, "")       // strip [ ]
    .replace(/['"]/g, "")          // strip quotes
    .trim()
    .split(/\s+/)                  // numpy arrays use spaces, not commas
    .filter(Boolean)
    .join(", ");
}

function normaliseResults(results: PresentationResult[]): PresentationResult[] {
  // Deduplicate by name+cuisines combo — same restaurant listed twice by LLM
  const seen = new Set<string>();
  return results
    .filter((r) => {
      const key = `${r.name}||${r.cuisines}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .map((r) => ({
      ...r,
      cuisines: cleanCuisines(r.cuisines),
    }));
}

export default function Home() {
  const [isLoading,    setIsLoading]    = useState(false);
  const [data,         setData]         = useState<PresentationResponse | null>(null);
  const [error,        setError]        = useState<string | null>(null);
  const [showResults,  setShowResults]  = useState(false);

  const handleSearch = async (prefs: UserPreferences) => {
    setIsLoading(true);
    setError(null);
    setData(null);
    setShowResults(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
    try {
      const raw = await getRecommendations(prefs);
      setData({
        ...raw,
        results: normaliseResults(raw.results),
      });
    } catch (err) {
      console.error(err);
      setError(
        `Couldn't reach the backend at ${API_BASE_URL}. ` +
        (process.env.NEXT_PUBLIC_API_URL
          ? "Please ensure the deployed backend is available."
          : "If you're deploying to Vercel, set NEXT_PUBLIC_API_URL in project settings.")
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setShowResults(false);
    setData(null);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-[#fbf9f8] text-[#1b1c1c] pb-20 md:pb-0">
      <Header />
      <Hero onSearch={handleSearch} isLoading={isLoading} />

      <AnimatePresence mode="wait">
        {!showResults ? (
          <motion.div
            key="discovery"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <TrendingSection />
            <CuisineCategories />
            <FeatureSection />
          </motion.div>
        ) : (
          <motion.div
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {/* Back button */}
            <div className="px-4 md:px-12 pt-6">
              <button
                onClick={handleBack}
                className="flex items-center gap-1.5 text-sm font-semibold text-[#b7122a] hover:underline underline-offset-2"
              >
                <span className="material-symbols-outlined text-[18px]" aria-hidden="true">
                  arrow_back
                </span>
                Back to explore
              </button>
            </div>

            {isLoading ? (
              <SkeletonLoader />
            ) : error ? (
              <div className="mx-4 md:mx-12 my-8 bg-[#ffdad6] border border-[#ba1a1a]/20 p-8 rounded-3xl text-center">
                <span className="material-symbols-outlined text-[#ba1a1a] text-5xl block mb-3" aria-hidden="true">
                  wifi_off
                </span>
                <p className="text-[#ba1a1a] font-semibold text-base mb-1">Something went wrong</p>
                <p className="text-[#5b403f] text-sm mb-5">{error}</p>
                <button
                  onClick={handleBack}
                  className="bg-[#b7122a] text-white text-sm font-semibold px-6 py-3 rounded-xl hover:bg-[#db313f] transition-colors"
                >
                  Try again
                </button>
              </div>
            ) : data && data.results.length > 0 ? (
              <RecommendationList data={data} />
            ) : data && data.results.length === 0 ? (
              <div className="mx-4 md:mx-12 my-8 text-center py-20">
                <span className="material-symbols-outlined text-[64px] text-[#e4bebc] block mb-4" aria-hidden="true">
                  search_off
                </span>
                <p className="text-[#1b1c1c] text-lg font-bold mb-2">No restaurants found</p>
                <p className="text-[#5b403f] text-sm mb-6">
                  Try a different city, lower your minimum rating, or broaden your cuisine.
                </p>
                <button
                  onClick={handleBack}
                  className="bg-[#b7122a] text-white text-sm font-semibold px-6 py-3 rounded-xl hover:bg-[#db313f] transition-colors"
                >
                  Search again
                </button>
              </div>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>

      <Footer />
      <MobileNavigation />
    </main>
  );
}
