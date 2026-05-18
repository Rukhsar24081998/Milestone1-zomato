"use client";

import React from "react";

export const FeatureSection: React.FC = () => {
  return (
    <section className="py-8 px-4 md:px-12 bg-[#f5f3f3] mb-8">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-8">
        <div className="flex-1 space-y-4">
          <h2 className="text-3xl font-bold text-[#1b1c1c]">
            Meet Zomato AI. Your new personal concierge.
          </h2>
          <p className="text-base text-[#5b403f]">
            We don't just show you restaurants. We understand your preferences, allergies, and price sensitivity to map out your perfect culinary journey.
          </p>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="material-symbols-outlined text-[#b7122a]" style={{ fontVariationSettings: "'FILL' 1" }}>
                check_circle
              </span>
              <div>
                <h4 className="text-sm font-semibold">Personalized Taste Profile</h4>
                <p className="text-sm opacity-70">Build your palate profile through quick flavor polls.</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="material-symbols-outlined text-[#b7122a]" style={{ fontVariationSettings: "'FILL' 1" }}>
                check_circle
              </span>
              <div>
                <h4 className="text-sm font-semibold">Group Recommendation Engine</h4>
                <p className="text-sm opacity-70">Pick a spot that everyone will love, automatically.</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <span className="material-symbols-outlined text-[#b7122a]" style={{ fontVariationSettings: "'FILL' 1" }}>
                check_circle
              </span>
              <div>
                <h4 className="text-sm font-semibold">Real-time Wait AI</h4>
                <p className="text-sm opacity-70">Accurate live prediction of wait times at popular spots.</p>
              </div>
            </li>
          </ul>
          <button className="bg-[#b7122a] text-white text-sm font-semibold px-6 py-4 rounded-xl shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all">
            Get AI Recommendations
          </button>
        </div>
        <div className="flex-1 relative">
          <div className="w-full aspect-square rounded-[48px] overflow-hidden shadow-2xl relative z-10">
            <img
              className="w-full h-full object-cover"
              alt="Happy group of friends sharing dishes at a restaurant"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAV2cU7C8hJmfA3_GdGsuN32nMJH-k_04LqVIPDeQ9lrAoTfRJTBM6UvkSM62WlHhjX8Qornb1PT1VFqIrZL7h3nxCoSid-5DdYwKxsCMFH0TqObIKIdWzoD13pAa-QJYlATdlx4mqwRwGM3vDRrOa-M4yuxbU3YY3WoifpL6PzcVrAqBPK3eQMQWiPGUPMwG6OBb9xxT7tc4tZa1tIEgWs0Z1SxnQ72uHJG6v0TG-O8tGGDKZVKNdwioxcubtxRkc0RJPyMNa5l_HS"
            />
          </div>
          <div className="absolute -top-6 -right-6 w-32 h-32 bg-[#db313f] rounded-3xl -z-0 opacity-20"></div>
          <div className="absolute -bottom-10 -left-10 w-48 h-48 border-[20px] border-[#e4bebc]/30 rounded-full -z-0"></div>
        </div>
      </div>
    </section>
  );
};
