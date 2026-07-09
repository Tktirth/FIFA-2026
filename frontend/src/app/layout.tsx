import type { Metadata, Viewport } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export const viewport: Viewport = {
  themeColor: "#09090b",
}

export const metadata: Metadata = {
  title: "NEXOVA | Intelligent Stadium OS",
  description: "The AI-powered operating system for the FIFA 2026 World Cup.",
  manifest: "/manifest.json",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.variable} font-sans h-full bg-[#fcfcfc] antialiased`}>
        {children}
      </body>
    </html>
  )
}
