"use client"

import { motion } from "motion/react"
import { Activity, Users, AlertCircle, ArrowUpRight, TrendingUp } from "lucide-react"
import dynamic from "next/dynamic"

const LiveCrowdChart = dynamic(() => import("@/components/dashboard/LiveCrowdChart"), { ssr: false })
const IncidentDistribution = dynamic(() => import("@/components/dashboard/IncidentDistribution"), { ssr: false })
const StadiumMapWrapper = dynamic(() => import("@/components/map/StadiumMapWrapper"), { ssr: false })

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <motion.h1 
          className="text-3xl font-semibold tracking-tight"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          Stadium Operations
        </motion.h1>
        <motion.p 
          className="text-muted-foreground mt-1"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.05 }}
        >
          Real-time intelligence and insights for MetLife Stadium.
        </motion.p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Metric 1 */}
        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div className="flex items-center justify-between">
            <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
              <Users className="h-5 w-5 text-primary" />
            </div>
            <div className="flex items-center gap-1 text-sm font-medium text-emerald-700 bg-emerald-50 px-2 py-1 rounded-md">
              <TrendingUp className="h-3 w-3" />
              +12%
            </div>
          </div>
          <div className="mt-4">
            <h2 className="text-muted-foreground text-sm font-medium">Current Attendance</h2>
            <p className="text-3xl font-semibold mt-1">68,402</p>
          </div>
        </motion.div>

        {/* Metric 2 */}
        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="flex items-center justify-between">
            <div className="h-10 w-10 rounded-full bg-orange-100 flex items-center justify-center">
              <AlertCircle className="h-5 w-5 text-orange-600" />
            </div>
            <span className="text-sm font-medium text-muted-foreground">3 Unresolved</span>
          </div>
          <div className="mt-4">
            <h2 className="text-muted-foreground text-sm font-medium">Active Incidents</h2>
            <p className="text-3xl font-semibold mt-1">12</p>
          </div>
        </motion.div>

        {/* Metric 3 */}
        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <div className="flex items-center justify-between">
            <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
              <Activity className="h-5 w-5 text-indigo-600" />
            </div>
            <span className="text-sm font-medium text-muted-foreground">Updated just now</span>
          </div>
          <div className="mt-4">
            <h2 className="text-muted-foreground text-sm font-medium">System Health Score</h2>
            <p className="text-3xl font-semibold mt-1">98.4</p>
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow h-96 flex flex-col"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-lg">AI Crowd Prediction</h2>
            <button className="text-sm text-primary hover:underline flex items-center gap-1">
              View details <ArrowUpRight className="h-3 w-3" />
            </button>
          </div>
          <div className="flex-1 w-full relative">
            <LiveCrowdChart />
          </div>
        </motion.div>

        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow h-96 flex flex-col"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-lg">AI Incident Insights</h2>
            <button className="text-sm text-primary hover:underline flex items-center gap-1">
              View log <ArrowUpRight className="h-3 w-3" />
            </button>
          </div>
          <div className="space-y-4 flex-1 overflow-auto pr-2" tabIndex={0} aria-label="Incident Insights Log">
            {[1, 2, 3].map((i) => (
              <div key={i} className="p-4 rounded-lg bg-secondary/50 border border-border">
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 h-2 w-2 rounded-full bg-orange-500 shrink-0"></div>
                  <div>
                    <h3 className="font-medium text-sm">Medical issue near Gate B</h3>
                    <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                      AI Summary: A fan has reported dehydration symptoms near concession 12. Medical team dispatched, ETA 2 mins.
                    </p>
                    <span className="text-xs text-foreground/80 mt-2 block uppercase tracking-wider font-semibold">4 mins ago</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow lg:col-span-2 flex flex-col"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-lg">Stadium Topography & Live Crowd</h2>
          </div>
          <div className="flex-1 relative rounded-xl overflow-hidden border border-border">
            <StadiumMapWrapper />
          </div>
        </motion.div>

        <motion.div 
          className="bg-card border border-border rounded-xl p-6 premium-shadow flex flex-col"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.7 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-lg">Incident Distribution</h2>
          </div>
          <div className="flex-1 w-full relative">
            <IncidentDistribution />
          </div>
        </motion.div>
      </div>
    </div>
  )
}
