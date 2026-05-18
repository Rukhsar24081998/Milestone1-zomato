import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";

/*
  Load Montserrat through next/font/google — this is the correct Next.js
  App Router approach. It self-hosts the font, eliminates the external
  request, and guarantees the font is available before first paint.
  The previous @import url() in globals.css and manual <link> tags both
  failed because Turbopack/App Router strips or de-prioritises them.
*/
const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-montserrat",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Zomato AI Recommendations | Find Your Perfect Restaurant",
  description:
    "Zomato AI's recommendation engine learns your unique palate to recommend the perfect restaurant, tailored to your mood and location.",
  /*
    Material Symbols cannot be loaded through next/font (it's a variable
    icon font, not a text font). The correct way to inject it in App Router
    is via the metadata `other` field which Next.js renders as <link> tags
    in the <head> before any JS hydration.
  */
  other: {
    "google-font-material-symbols": "",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${montserrat.variable} h-full antialiased`}>
      <head>
        {/*
          Material Symbols must be a real <link> in <head>.
          Next.js App Router allows <link> tags directly inside <head>
          when placed here in the RootLayout — they are NOT stripped.
          Using `display=block` (not swap) prevents the FOUT where icon
          codepoints flash as text before the font loads.
        */}
        <link
          rel="preconnect"
          href="https://fonts.googleapis.com"
        />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block"
        />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
