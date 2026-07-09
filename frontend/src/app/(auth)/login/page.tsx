"use client"

import { useState } from "react"
import { motion } from "motion/react"
import { useRouter } from "next/navigation"
import { 
  User, HeartHandshake, Shield, Cross, Activity, 
  Store, Trash, Bus, Star, Camera, ChevronRight 
} from "lucide-react"

const PERSONAS = [
  { id: "fan", name: "Fan", desc: "Match info & Navigation", icon: User, color: "bg-blue-500/10 text-blue-600 border-blue-500/20" },
  { id: "volunteer", name: "Volunteer", desc: "Shift tasks & Alerts", icon: HeartHandshake, color: "bg-green-500/10 text-green-600 border-green-500/20" },
  { id: "security", name: "Security", desc: "Crowd & Incidents", icon: Shield, color: "bg-red-500/10 text-red-600 border-red-500/20" },
  { id: "medical", name: "Medical", desc: "Health incidents", icon: Cross, color: "bg-red-500/10 text-red-600 border-red-500/20" },
  { id: "operations", name: "Operations", desc: "Stadium Pulse", icon: Activity, color: "bg-purple-500/10 text-purple-600 border-purple-500/20" },
  { id: "vendor", name: "Vendor", desc: "Queues & Stock", icon: Store, color: "bg-orange-500/10 text-orange-600 border-orange-500/20" },
  { id: "cleaning", name: "Cleaning", desc: "Waste tracking", icon: Trash, color: "bg-emerald-500/10 text-emerald-600 border-emerald-500/20" },
  { id: "transport", name: "Transport", desc: "Parking & Traffic", icon: Bus, color: "bg-yellow-500/10 text-yellow-600 border-yellow-500/20" },
  { id: "vip", name: "VIP", desc: "Concierge access", icon: Star, color: "bg-amber-500/10 text-amber-600 border-amber-500/20" },
  { id: "media", name: "Media", desc: "Press information", icon: Camera, color: "bg-indigo-500/10 text-indigo-600 border-indigo-500/20" },
]

export default function LoginPage() {
  const router = useRouter()
  const [selected, setSelected] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    if (!selected) return
    
    setIsLoading(true)
    // Simulate auth request
    setTimeout(() => {
      // In real app, we would store token here
      router.push("/")
    }, 800)
  }

  return (
    <main className="min-h-screen bg-background flex flex-col justify-center items-center p-4">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-12">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, type: "spring" }}
            className="inline-flex h-16 w-16 rounded-2xl bg-foreground items-center justify-center mb-6 premium-shadow"
          >
            <span className="text-background font-bold text-2xl tracking-tighter">NX</span>
          </motion.div>
          <motion.h1 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl font-semibold tracking-tight"
          >
            Welcome to NEXOVA
          </motion.h1>
          <motion.p 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-muted-foreground mt-3 text-lg"
          >
            Select your persona to enter the demo environment
          </motion.p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            {PERSONAS.map((persona, i) => (
              <motion.button
                key={persona.id}
                type="button"
                onClick={() => setSelected(persona.id)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 + i * 0.05 }}
                className={`flex flex-col items-center justify-center p-6 rounded-xl border text-center transition-all ${
                  selected === persona.id 
                    ? "border-primary ring-2 ring-primary/20 bg-primary/5 premium-shadow scale-105 z-10" 
                    : "border-border bg-card hover:border-primary/30 hover:bg-secondary/50"
                }`}
              >
                <div className={`h-12 w-12 rounded-full flex items-center justify-center border mb-4 ${persona.color}`}>
                  <persona.icon className="h-6 w-6" />
                </div>
                <h2 className="font-medium text-sm">{persona.name}</h2>
                <p className="text-xs text-muted-foreground mt-1 hidden md:block">{persona.desc}</p>
              </motion.button>
            ))}
          </div>

          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="flex justify-center"
          >
            <button
              type="submit"
              disabled={!selected || isLoading}
              className={`h-12 px-8 rounded-full font-medium flex items-center gap-2 transition-all ${
                selected && !isLoading
                  ? "bg-primary text-primary-foreground hover:opacity-90 premium-shadow"
                  : "bg-secondary text-muted-foreground cursor-not-allowed"
              }`}
            >
              {isLoading ? "Authenticating..." : "Enter Platform"}
              {!isLoading && <ChevronRight className="h-4 w-4" />}
            </button>
          </motion.div>
        </form>
      </div>
    </main>
  )
}
