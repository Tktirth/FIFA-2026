"use client"

import { motion } from "motion/react"
import { Users } from "lucide-react"

export default function CrowdPage() {
  return (
    <div className="space-y-8">
      <div>
        <motion.h1 
          className="text-3xl font-semibold tracking-tight"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          Crowd Status
        </motion.h1>
        <motion.p 
          className="text-muted-foreground mt-1"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.05 }}
        >
          Real-time density analysis and crowd predictions.
        </motion.p>
      </div>

      <motion.div 
        className="bg-card border border-border rounded-xl p-8 premium-shadow min-h-[500px] flex items-center justify-center flex-col text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="h-16 w-16 rounded-full bg-indigo-100 flex items-center justify-center mb-4">
          <Users className="h-8 w-8 text-indigo-600" />
        </div>
        <h2 className="text-xl font-semibold">Crowd Analytics</h2>
        <p className="text-muted-foreground mt-2 max-w-md">
          Detailed crowd density data is being processed by the intelligence engine.
        </p>
      </motion.div>
    </div>
  )
}
