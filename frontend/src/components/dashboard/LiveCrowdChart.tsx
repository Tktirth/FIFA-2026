"use client";

import { useMemo } from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';
import { useFirestoreRealtime } from '@/lib/use-firestore-realtime';

export default function LiveCrowdChart() {
  const { data } = useFirestoreRealtime('crowd_density');

  // Format data for the chart: aggregate by time
  const chartData = useMemo(() => {
    if (!data || data.length === 0) {
      // Mock data if no real data is flowing yet
      return [
        { time: '10:00', total: 12000 },
        { time: '10:30', total: 25000 },
        { time: '11:00', total: 45000 },
        { time: '11:30', total: 68000 },
        { time: '12:00', total: 82000 },
        { time: '12:30', total: 80500 },
      ];
    }
    
    // Group by timestamp in a real scenario
    // For now, since the hook fetches all historical, we can map it
    return data
      .slice(-20) // take latest 20
      .map(d => ({
        time: d.timestamp ? new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 'Now',
        total: d.current_occupancy || 0
      }));
  }, [data]);

  return (
    <div className="h-[300px] w-full mt-4">

      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={chartData}
          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
          <XAxis 
            dataKey="time" 
            stroke="#525252" 
            tick={{ fill: '#737373', fontSize: 12 }} 
            tickLine={false}
            axisLine={false}
            dy={10}
          />
          <YAxis 
            stroke="#525252" 
            tick={{ fill: '#737373', fontSize: 12 }} 
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `${value / 1000}k`}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#171717', 
              border: '1px solid #262626',
              borderRadius: '8px',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)'
            }}
            itemStyle={{ color: '#f5f5f5' }}
            labelStyle={{ color: '#a3a3a3', marginBottom: '4px' }}
          />
          <Area 
            type="monotone" 
            dataKey="total" 
            stroke="#3b82f6" 
            strokeWidth={3}
            fillOpacity={1} 
            fill="url(#colorTotal)" 
            animationDuration={1500}
            activeDot={{ r: 6, fill: '#3b82f6', stroke: '#171717', strokeWidth: 2 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
