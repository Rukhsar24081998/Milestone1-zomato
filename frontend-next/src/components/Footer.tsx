"use client";

import React, { useState } from "react";

export const Footer: React.FC = () => {
  const [email, setEmail] = useState("");

  const handleSubscribe = () => {
    if (email) {
      alert(`Subscribed with: ${email}`);
      setEmail("");
    }
  };

  return (
    <footer className="bg-[#303031] text-[#f2f0f0] py-8 px-4 md:px-12">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="col-span-1 md:col-span-1">
          <div className="flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined text-[#ffb3b1] text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
              restaurant_menu
            </span>
            <span className="text-xl font-bold tracking-tight">ZOMATO AI</span>
          </div>
          <p className="text-sm opacity-70 mb-6">Revolutionizing how the world eats, one bite at a time.</p>
          <div className="flex gap-4">
            <span className="material-symbols-outlined opacity-60 hover:opacity-100 cursor-pointer">public</span>
            <span className="material-symbols-outlined opacity-60 hover:opacity-100 cursor-pointer">language</span>
            <span className="material-symbols-outlined opacity-60 hover:opacity-100 cursor-pointer">share</span>
          </div>
        </div>
        <div>
          <h4 className="text-sm font-semibold text-[#ffb3b1] mb-4">For Foodies</h4>
          <ul className="space-y-2 text-sm opacity-70">
            <li className="hover:text-[#ffb3b1] cursor-pointer">Zomato AI Profile</li>
            <li className="hover:text-[#ffb3b1] cursor-pointer">Foodie Communities</li>
            <li className="hover:text-[#ffb3b1] cursor-pointer">Mobile App</li>
            <li className="hover:text-[#ffb3b1] cursor-pointer">Taste Rewards</li>
          </ul>
        </div>
        <div>
          <h4 className="text-sm font-semibold text-[#ffb3b1] mb-4">For Restaurants</h4>
          <ul className="space-y-2 text-sm opacity-70">
            <li className="hover:text-[#ffb3b1] cursor-pointer">Partner with Us</li>
            <li className="hover:text-[#ffb3b1] cursor-pointer">Business Dashboard</li>
            <li className="hover:text-[#ffb3b1] cursor-pointer">Marketing Tools</li>
            <li className="hover:text-[#ffb3b1] cursor-pointer">Kitchen AI</li>
          </ul>
        </div>
        <div>
          <h4 className="text-sm font-semibold text-[#ffb3b1] mb-4">Newsletter</h4>
          <p className="text-sm opacity-70 mb-2">Get weekly hidden gems in NYC.</p>
          <div className="flex bg-white/10 rounded-lg p-1">
            <input
              className="bg-transparent border-none focus:ring-0 text-white flex-1 text-xs px-2"
              placeholder="email@example.com"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <button
              onClick={handleSubscribe}
              className="bg-[#db313f] px-3 py-1 rounded text-white text-xs font-bold"
            >
              Join
            </button>
          </div>
        </div>
      </div>
      <div className="mt-8 pt-6 border-t border-white/10 text-center text-xs opacity-50">
        © {new Date().getFullYear()} Zomato AI Recommendations. All rights reserved.
      </div>
    </footer>
  );
};
