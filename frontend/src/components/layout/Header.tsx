"use client"

import { Bell, Search } from "lucide-react"

export function Header() {
  return (
    <header className="h-16 glass sticky top-0 z-40 flex items-center justify-between px-6 border-b border-border">
      <div className="flex items-center flex-1 gap-4">
        <div className="relative w-96 hidden md:block">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search zones, incidents, volunteers..."
            className="w-full bg-secondary/50 border border-transparent rounded-md h-9 pl-9 pr-4 text-sm focus:outline-none focus:border-border focus:bg-background transition-colors placeholder:text-muted-foreground"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/50 border border-border text-xs font-medium">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          System Optimal
        </div>
        
        <button className="relative h-9 w-9 rounded-full hover:bg-secondary flex items-center justify-center transition-colors text-muted-foreground hover:text-foreground" aria-label="Notifications">
          <Bell className="h-4 w-4" />
          <span className="absolute top-2 right-2.5 h-1.5 w-1.5 rounded-full bg-primary ring-2 ring-background"></span>
        </button>
      </div>
    </header>
  )
}
