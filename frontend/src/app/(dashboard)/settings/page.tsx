"use client"

import { motion } from "motion/react"
import { Settings, Save, Shield, BellRing, Smartphone } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="space-y-8">
      <div>
        <motion.h1 
          className="text-3xl font-semibold tracking-tight"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          System Settings
        </motion.h1>
        <motion.p 
          className="text-muted-foreground mt-1"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.05 }}
        >
          Manage NEXOVA platform configuration and preferences.
        </motion.p>
      </div>

      <motion.div 
        className="bg-card border border-border rounded-xl p-8 premium-shadow"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="space-y-6">
          
          <div className="flex items-center justify-between pb-6 border-b border-border">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                <BellRing className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-medium text-lg">Push Notifications</h3>
                <p className="text-sm text-muted-foreground">Manage automated incident alerts.</p>
              </div>
            </div>
            <button className="px-4 py-2 bg-secondary text-secondary-foreground font-medium rounded-md hover:bg-secondary/80 transition-colors">
              Configure
            </button>
          </div>

          <div className="flex items-center justify-between pb-6 border-b border-border">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-emerald-100 flex items-center justify-center">
                <Shield className="h-6 w-6 text-emerald-600" />
              </div>
              <div>
                <h3 className="font-medium text-lg">Access Control</h3>
                <p className="text-sm text-muted-foreground">Manage team permissions and roles.</p>
              </div>
            </div>
            <button className="px-4 py-2 bg-secondary text-secondary-foreground font-medium rounded-md hover:bg-secondary/80 transition-colors">
              Manage Roles
            </button>
          </div>

          <div className="flex items-center justify-between pb-6 border-b border-border">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center">
                <Smartphone className="h-6 w-6 text-indigo-600" />
              </div>
              <div>
                <h3 className="font-medium text-lg">Device Integration</h3>
                <p className="text-sm text-muted-foreground">Manage connected IoT sensors.</p>
              </div>
            </div>
            <button className="px-4 py-2 bg-secondary text-secondary-foreground font-medium rounded-md hover:bg-secondary/80 transition-colors">
              View Devices
            </button>
          </div>

          <div className="pt-4 flex justify-end">
            <button className="flex items-center gap-2 px-6 py-2 bg-primary text-primary-foreground font-medium rounded-md hover:bg-primary/90 transition-colors">
              <Save className="h-4 w-4" />
              Save Changes
            </button>
          </div>

        </div>
      </motion.div>
    </div>
  )
}
