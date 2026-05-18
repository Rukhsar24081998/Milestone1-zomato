"use client";

import React, { useState } from "react";

export const CuisineCategories: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState("Steak");

  const categories = [
    { name: "Pizza", icon: "local_pizza" },
    { name: "Ramen", icon: "ramen_dining" },
    { name: "Steak", icon: "dinner_dining" },
    { name: "Bakery", icon: "bakery_dining" },
    { name: "Seafood", icon: "set_meal" },
    { name: "Desserts", icon: "icecream" },
    { name: "Coffee", icon: "local_cafe" },
  ];

  return (
    <section className="py-8 px-4 md:px-12 overflow-hidden">
      <h2 className="text-2xl font-bold text-[#1b1c1c] mb-6">What are you craving?</h2>
      <div className="flex gap-4 overflow-x-auto pb-4 no-scrollbar">
        {categories.map((category) => (
          <div
            key={category.name}
            className="flex-shrink-0 flex flex-col items-center gap-2 group cursor-pointer"
            onClick={() => setSelectedCategory(category.name)}
          >
            <div
              className={`w-20 h-20 rounded-full flex items-center justify-center transition-all group-hover:shadow-lg ${
                selectedCategory === category.name
                  ? "bg-[#b7122a] shadow-lg"
                  : "bg-[#e9e8e7]"
              }`}
            >
              <span
                className={`material-symbols-outlined text-4xl ${
                  selectedCategory === category.name ? "text-white" : "text-[#5b403f]"
                }`}
              >
                {category.icon}
              </span>
            </div>
            <span
              className={`text-sm font-semibold ${
                selectedCategory === category.name ? "text-[#b7122a]" : ""
              }`}
            >
              {category.name}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
};
