import type { Metadata, Viewport } from "next";
import { Kantumruy_Pro } from "next/font/google";
import "./globals.css";

const kantumruy = Kantumruy_Pro({
  variable: "--font-kantumruy",
  subsets: ["khmer"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: {
    template: "%s | កាលវិភាគសាលា",
    default: "កាលវិភាគសាលា",
  },
  description: "បុគ្គលិកកាលវិភាគសាលា ដោយ វិទ្យាល័យ សាកល្បង (NGIS)",
  openGraph: { siteName: "កាលវិភាគសាលា - NGIS", locale: "km_KH", type: "website" },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="km" className={`${kantumruy.variable} h-full antialiased`}>
      <head>
        <meta charSet="utf-8" />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
