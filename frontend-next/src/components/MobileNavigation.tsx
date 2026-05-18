"use client";

import React from "react";

export const MobileNavigation: React.FC = () => {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-2 py-3 pb-safe bg-[#fbf9f8] shadow-[0_-4px_12px_rgba(0,0,0,0.05)] rounded-t-xl transition-all">
      <div className="flex flex-col items-center justify-center bg-[#db313f] text-white rounded-xl px-4 py-1 active:scale-90 duration-200 transition-transform">
        <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
          home
        </span>
        <span className="text-xs font-semibold">Home</span>
      </div>
      <div className="flex flex-col items-center justify-center text-[#5f5e5e] px-4 py-1 active:scale-90 duration-200 transition-transform">
        <span className="material-symbols-outlined">bookmarks</span>
        <span className="text-xs font-semibold">Collections</span>
      </div>
      <div className="flex flex-col items-center justify-center text-[#5f5e5e] px-4 py-1 active:scale-90 duration-200 transition-transform">
        <span className="material-symbols-outlined">person</span>
        <span className="text-xs font-semibold">Profile</span>
      </div>
    </nav>
  );
};
