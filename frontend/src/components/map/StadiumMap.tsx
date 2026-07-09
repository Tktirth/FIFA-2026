"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Popup, Circle } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useFirestoreRealtime } from "@/lib/use-firestore-realtime";

// Fix Leaflet's default icon path issues in Next.js
const defaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = defaultIcon;

// New York MetLife Stadium Coordinates (Approximate for demo)
const STADIUM_CENTER: [number, number] = [40.8135, -74.0745];

interface ZoneDensity {
  id: string;
  zone_id: string;
  current_occupancy: number;
  capacity: number;
  percentage: number;
  level: "LOW" | "MODERATE" | "HIGH" | "CRITICAL";
  timestamp?: string;
}

const ZONE_COORDS: Record<string, [number, number]> = {
  "north_gate": [40.8150, -74.0745],
  "south_gate": [40.8120, -74.0745],
  "food_court_a": [40.8135, -74.0760],
  "merch_shop_1": [40.8135, -74.0730],
  "vip_lounge": [40.8145, -74.0755],
  "medical_tent": [40.8125, -74.0735],
};

const getColorForLevel = (level: string) => {
  switch (level) {
    case "LOW": return "#10b981"; // Emerald 500
    case "MODERATE": return "#f59e0b"; // Amber 500
    case "HIGH": return "#ef4444"; // Red 500
    case "CRITICAL": return "#7f1d1d"; // Red 900
    default: return "#3b82f6"; // Blue 500
  }
};

export default function StadiumMap() {
  const [mounted, setMounted] = useState(false);
  const { data: zones } = useFirestoreRealtime<ZoneDensity>("crowd_density");

  // Fix hydration issues with Leaflet
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setMounted(true);
  }, []);

  if (!mounted) return <div className="h-[400px] w-full rounded-2xl bg-neutral-900 animate-pulse flex items-center justify-center text-neutral-500">Loading Map...</div>;

  // Deduplicate zones to only show the latest reading per zone
  const latestZones: Record<string, ZoneDensity> = {};
  zones?.forEach(z => {
    if (!latestZones[z.zone_id] || (z.timestamp && latestZones[z.zone_id].timestamp && z.timestamp > latestZones[z.zone_id].timestamp!)) {
      latestZones[z.zone_id] = z;
    }
  });

  return (
    <div className="h-[500px] w-full rounded-2xl overflow-hidden shadow-2xl ring-1 ring-white/10 relative isolate">
      {/* Premium dark glass overlay effect on edges */}
      <div className="absolute inset-0 z-[1000] pointer-events-none shadow-[inset_0_0_50px_rgba(0,0,0,0.8)]" />
      
      <MapContainer 
        center={STADIUM_CENTER} 
        zoom={16} 
        scrollWheelZoom={true}
        className="h-full w-full bg-[#0d1117] z-0"
        zoomControl={false}
      >
        {/* CartoDB Dark Matter Base Map - Premium & Free */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />

        {/* Render Crowd Heatmap Circles */}
        {Object.values(latestZones).map((zone) => {
          const coords = ZONE_COORDS[zone.zone_id];
          if (!coords) return null;
          
          const color = getColorForLevel(zone.level);

          return (
            <Circle
              key={zone.id}
              center={coords}
              radius={30 + (zone.percentage * 0.5)} // Dynamic size
              pathOptions={{
                color: color,
                fillColor: color,
                fillOpacity: 0.4,
                weight: 2,
              }}
            >
              <Popup className="premium-popup">
                <div className="p-1 min-w-[150px]">
                  <h4 className="font-bold text-lg mb-1 capitalize text-neutral-900">
                    {zone.zone_id.replace("_", " ")}
                  </h4>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs text-neutral-500 uppercase font-semibold">Status</span>
                    <span style={{ color }} className="text-xs font-bold uppercase">{zone.level}</span>
                  </div>
                  <div className="w-full bg-neutral-200 rounded-full h-1.5 mb-2">
                    <div className="h-1.5 rounded-full" style={{ width: `${zone.percentage}%`, backgroundColor: color }}></div>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="font-medium text-neutral-700">{zone.current_occupancy}</span>
                    <span className="text-neutral-400">/ {zone.capacity}</span>
                  </div>
                </div>
              </Popup>
            </Circle>
          );
        })}
      </MapContainer>
    </div>
  );
}
