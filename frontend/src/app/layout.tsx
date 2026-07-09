import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export const metadata: Metadata = {
  title: "NEXOVA | Intelligent Stadium OS",
  description: "The AI-powered operating system for the FIFA 2026 World Cup.",
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
