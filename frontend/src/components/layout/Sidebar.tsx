"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { motion } from "motion/react"
import { 
  LayoutDashboard, 
  Map, 
  Users, 
  AlertTriangle, 
  Settings,
  Activity,
  HeartHandshake
} from "lucide-react"

import { cn } from "@/lib/utils"

const NAV_ITEMS = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Navigation", href: "/navigation", icon: Map },
  { name: "Crowd Status", href: "/crowd", icon: Users },
  { name: "Incidents", href: "/incidents", icon: AlertTriangle },
  { name: "Volunteers", href: "/volunteers", icon: HeartHandshake },
  { name: "Pulse", href: "/pulse", icon: Activity },
  { name: "Settings", href: "/settings", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 border-r border-border bg-background flex flex-col h-screen sticky top-0">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-sm tracking-tighter">NX</span>
          </div>
          <span className="font-semibold text-lg tracking-tight">NEXOVA</span>
        </div>
      </div>
      
      <nav className="flex-1 overflow-y-auto py-6 px-3 space-y-1">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`) && item.href !== "/"
          
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md transition-colors relative group text-sm font-medium",
                isActive 
                  ? "text-primary" 
                  : "text-muted-foreground hover:text-foreground hover:bg-secondary/50"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active"
                  className="absolute inset-0 bg-secondary rounded-md -z-10"
                  initial={false}
                  transition={{ type: "spring", stiffness: 400, damping: 30 }}
                />
              )}
              <item.icon className={cn("h-4 w-4", isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground")} />
              {item.name}
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 px-3 py-2 rounded-md bg-secondary/50">
          <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
            <span className="text-xs font-medium text-primary">OM</span>
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-medium leading-none">Ops Manager</span>
            <span className="text-xs text-muted-foreground mt-1">Admin Access</span>
          </div>
        </div>
      </div>
    </aside>
  )
}
