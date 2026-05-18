"use client";

import React from "react";

export const TrendingSection: React.FC = () => {
  return (
    <section className="py-8 px-4 md:px-12 bg-[#fbf9f8]">
      <div className="flex flex-col md:flex-row justify-between items-end mb-6 gap-4">
        <div>
          <span className="text-[#b7122a] text-sm font-semibold uppercase tracking-widest mb-2 block">
            Curation for you
          </span>
          <h2 className="text-2xl font-bold text-[#1b1c1c]">Trending in NYC Right Now</h2>
        </div>
        <button className="text-[#b7122a] text-sm font-semibold flex items-center gap-1 hover:underline">
          View all collections <span className="material-symbols-outlined">arrow_forward</span>
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-6 lg:col-span-8 group relative h-[400px] rounded-3xl overflow-hidden shadow-lg">
          <img
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
            alt="A high-end modern restaurant interior with elegant wooden tables and warm overhead pendant lighting."
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDOk-z5Q8kKyEYHOv7-bgqlRp9PxCP9oiAbc9dZr5MDqSldWDk29pU8lc-OefYmOXELyFcAgAdjZuOcXEwi1WQzrqqm39KorlgF-7biGFKLpR9frPz3VRRLPxm6jHSN4NRhz4ax_hYmt0rRhvG_AVXf0D5CEh6_0mgDLA23VFZbYyONmZQVIKk-B6PM2njTy_xCekxR1878D3YjOsDuC1juX0nfvBI4T4k8u_khiHiyFC-O8da5qKqsFTWkoirDmcwCcF3C9TGepDwQ"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
          <div className="absolute bottom-0 left-0 p-6 text-white">
            <div className="flex gap-2 mb-2">
              <span className="bg-green-600 text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">
                Top Rated
              </span>
              <span className="bg-[#b7122a] text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">
                Trending
              </span>
            </div>
            <h3 className="text-xl font-bold mb-1">The Gilded Fork</h3>
            <p className="text-sm opacity-80 mb-4 max-w-md">
              Authentic Italian-American fusion in the heart of Chelsea. Known for the legendary Wagyu Meatballs.
            </p>
            <div className="flex items-center gap-4 text-xs">
              <span className="flex items-center gap-1">
                <span className="material-symbols-outlined text-sm text-yellow-400" style={{ fontVariationSettings: "'FILL' 1" }}>
                  star
                </span>{" "}
                4.9 (1.2k)
              </span>
              <span className="flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">schedule</span> 20-30 min
              </span>
              <span className="flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">distance</span> 0.8 miles
              </span>
            </div>
          </div>
        </div>
        <div className="md:col-span-6 lg:col-span-4 flex flex-col gap-6">
          <div className="group relative h-[188px] rounded-3xl overflow-hidden shadow-lg">
            <img
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              alt="Artisanal cocktails on a polished marble bar top."
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCBq31oaTOYsbMoMZZRdEORBeh7iqClqjh0fv3dPen7moNizNplykgKiZraE54C9OD-vSwYN_V8GuGg3bUUS4nPf9qLbpe8JHv15gquAeMlLuDeaOt_6YjP_rvYyrdD3AqSa9WhUAEj32Tpp8doKUEu41ZPx8xP6pShbE34tekpkmmdEDkcPnuyj7xdHg4VyWbJmH30Zs5bLqNIMO6HMrop-NdZM9tzv9YLO0RQznF6CX_J5DbjzCUzqvdPWRAmcuQnXmjujNY1CQZz"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
            <div className="absolute bottom-0 left-0 p-4 text-white">
              <h3 className="text-lg font-bold">Midnight Mixology</h3>
              <p className="text-xs opacity-80">Best Rooftop Cocktails & Tapas</p>
            </div>
          </div>
          <div className="group relative h-[188px] rounded-3xl overflow-hidden shadow-lg">
            <img
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              alt="Gourmet burger and golden fries on a minimalist black ceramic plate."
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuA7_YQLARGnNHl4Lr9fJK0LailHqAwvaJ78euQBTn2v8IIcawfQrwjBhglLB_JUWRa5IOxs-nlq0yYBFbsFo-xIMri7FpBqdnsYs4pzNCTBGTBAOz3NJN8cehC6eSqVofXRjn6v7IbzHka4lZIjI6-U9zq47eXxUGhaaxUo6sLfvoyeQ9PlxlNw3PaVVEJUotzSVJtp9bFBtnkuuQUNCOzFlf0epINIJgnVjekxT5xMDe7I1edC9CG-5ivPjb3jjnyblMgYi11YPYZw"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
            <div className="absolute bottom-0 left-0 p-4 text-white">
              <h3 className="text-lg font-bold">Neo-Bistro Burgers</h3>
              <p className="text-xs opacity-80">Gourmet Casual Selections</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
