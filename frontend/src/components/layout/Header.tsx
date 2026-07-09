"use client"

import { useState, useRef, useEffect } from "react"
import { Bell, Search, Info, AlertTriangle } from "lucide-react"

export function Header() {
  const [showNotifications, setShowNotifications] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const [unreadCount, setUnreadCount] = useState(2)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent | TouchEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowNotifications(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    document.addEventListener("touchstart", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
      document.removeEventListener("touchstart", handleClickOutside)
    }
  }, [])

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
      
      <div className="flex items-center gap-4 relative" ref={dropdownRef}>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/50 border border-border text-xs font-medium">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          System Optimal
        </div>
        
        <button 
          onClick={() => setShowNotifications((prev) => !prev)}
          className="relative h-9 w-9 rounded-full hover:bg-secondary flex items-center justify-center transition-colors text-muted-foreground hover:text-foreground" 
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          {unreadCount > 0 && (
            <span className="absolute top-2 right-2.5 h-1.5 w-1.5 rounded-full bg-primary ring-2 ring-background"></span>
          )}
        </button>

        {showNotifications && (
          <div className="absolute top-12 right-0 w-80 bg-background border border-border rounded-lg shadow-lg overflow-hidden flex flex-col z-50">
            <div className="px-4 py-3 border-b border-border bg-secondary/30">
              <h3 className="font-semibold text-sm">Notifications</h3>
            </div>
            <div className="max-h-[300px] overflow-y-auto">
              {unreadCount > 0 ? (
                <>
                  <a href="/incidents" onClick={() => setShowNotifications(false)} className="block px-4 py-3 border-b border-border/50 hover:bg-secondary/20 transition-colors flex gap-3 cursor-pointer">
                    <div className="mt-0.5 h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                      <Info className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">Simulation Data Generated</p>
                      <p className="text-xs text-muted-foreground mt-0.5">New crowd metrics are available for Zone B.</p>
                      <p className="text-[10px] text-muted-foreground mt-1">2 mins ago</p>
                    </div>
                  </a>
                  <a href="/incidents" onClick={() => setShowNotifications(false)} className="block px-4 py-3 hover:bg-secondary/20 transition-colors flex gap-3 cursor-pointer">
                    <div className="mt-0.5 h-8 w-8 rounded-full bg-orange-500/10 flex items-center justify-center shrink-0">
                      <AlertTriangle className="h-4 w-4 text-orange-500" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">Minor Incident Resolved</p>
                      <p className="text-xs text-muted-foreground mt-0.5">Gate C security alert has been cleared.</p>
                      <p className="text-[10px] text-muted-foreground mt-1">15 mins ago</p>
                    </div>
                  </a>
                </>
              ) : (
                <div className="px-4 py-6 text-center text-sm text-muted-foreground">
                  No new notifications
                </div>
              )}
            </div>
            <div className="px-4 py-2 border-t border-border bg-secondary/30 text-center">
              <button 
                onClick={() => { setUnreadCount(0); setShowNotifications(false); }}
                className="text-xs text-primary font-medium hover:underline disabled:opacity-50"
                disabled={unreadCount === 0}
              >
                Mark all as read
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}
