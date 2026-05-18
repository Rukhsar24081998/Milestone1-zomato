"use client";

import React, { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";

export const Header = () => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await checkHealth();
        setIsHealthy(data.status === "healthy");
      } catch {
        setIsHealthy(false);
      }
    };
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="flex justify-between items-center px-4 md:px-12 h-16 w-full sticky top-0 z-50 bg-[#fbf9f8] shadow-sm transition-colors">
      {/* Brand */}
      <div className="flex items-center gap-2">
        <span className="material-symbols-outlined text-[#b7122a] text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
          restaurant_menu
        </span>
        <span className="text-2xl font-black text-[#b7122a] tracking-tight">ZOMATO AI</span>
      </div>

      {/* Desktop Nav */}
      <div className="hidden md:flex items-center gap-6">
        <nav className="flex gap-4">
          <a href="#" className="text-sm font-semibold text-[#b7122a] px-3 py-1 bg-[#b7122a]/10 rounded-xl">Home</a>
          <a href="#discover" className="text-sm font-semibold text-[#5b403f] hover:text-[#b7122a] transition-colors px-3 py-1">Discover</a>
          <a href="#ai" className="text-sm font-semibold text-[#5b403f] hover:text-[#b7122a] transition-colors px-3 py-1">Zomato AI</a>
        </nav>

        {/* Health Indicator */}
        <div className="flex items-center gap-2 bg-[#efeded] px-3 py-1.5 rounded-full text-xs font-semibold">
          <div className="relative flex h-2 w-2">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isHealthy ? 'bg-[#48BB78]' : 'bg-red-500'}`}></span>
            <span className={`relative inline-flex rounded-full h-2 w-2 ${isHealthy ? 'bg-[#48BB78]' : 'bg-red-500'}`}></span>
          </div>
          <span className="text-[#5b403f] uppercase tracking-wider text-[10px]">
            {isHealthy === null ? "Checking..." : isHealthy ? "API Live" : "Offline"}
          </span>
        </div>
      </div>

      {/* Mobile Menu Button */}
      <button
        className="md:hidden p-2 text-[#5b403f]"
        onClick={() => setMenuOpen(!menuOpen)}
        aria-label="Toggle menu"
      >
        <span className="material-symbols-outlined">{menuOpen ? "close" : "menu"}</span>
      </button>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="absolute top-16 left-0 w-full bg-[#fbf9f8] shadow-lg border-t border-[#e4bebc] flex flex-col gap-2 px-4 py-4 md:hidden z-50">
          <a href="#" className="text-sm font-semibold text-[#b7122a] py-2 border-b border-[#efeded]">Home</a>
          <a href="#discover" className="text-sm font-semibold text-[#5b403f] py-2 border-b border-[#efeded]" onClick={() => setMenuOpen(false)}>Discover</a>
          <a href="#ai" className="text-sm font-semibold text-[#5b403f] py-2" onClick={() => setMenuOpen(false)}>Zomato AI</a>
        </div>
      )}
    </header>
  );
};
