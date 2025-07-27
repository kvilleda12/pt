import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PTI",
  description: "PTI is an AI powered bot that helps you with physical therapy in many ways. It gives you excersices you can do after telling it what body part you have problems with, guides you through excersices and analyzes them if you are doing them correctly. It also helps track a variety of data that can be used by others to hopefully revolutionize a sector or sectors fo the body.",
  openGraph: {
    title: "PTI | AI Physical Therapy Assistant",
    description: "PTI is an AI-powered bot for physical therapy: get personalized exercises, guidance, and progress tracking.",
    url: "https://pti.example.com/", // TODO: Replace with your actual URL
    siteName: "PTI",
    images: [
      {
        url: "/logo.png",
        width: 400,
        height: 400,
        alt: "PTI Logo"
      }
    ],
    locale: "en_US",
    type: "website"
  },
  twitter: {
    card: "summary_large_image",
    title: "PTI | AI Physical Therapy Assistant",
    description: "PTI is an AI-powered bot for physical therapy: get personalized exercises, guidance, and progress tracking.",
    images: [
      "/logo.png"
    ]
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
