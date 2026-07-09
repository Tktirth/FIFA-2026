"use client";

import { useMemo } from 'react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip,
  Legend
} from 'recharts';
import { useFirestoreRealtime } from '@/lib/use-firestore-realtime';

const COLORS = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'];

export default function IncidentDistribution() {
  const { data: incidents } = useFirestoreRealtime('incidents');

  const chartData = useMemo(() => {
    if (!incidents || incidents.length === 0) {
      return [
        { name: 'Medical', value: 4 },
        { name: 'Security', value: 3 },
        { name: 'Crowd', value: 2 },
        { name: 'Facilities', value: 1 },
      ];
    }

    const counts: Record<string, number> = {};
    incidents.forEach(inc => {
      const type = inc.type || 'Other';
      counts[type] = (counts[type] || 0) + 1;
    });

    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [incidents]);

  return (
    <div className="h-[280px] w-full mt-2">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="45%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={5}
            dataKey="value"
            stroke="none"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#171717', 
              border: '1px solid #262626',
              borderRadius: '8px',
            }}
            itemStyle={{ color: '#f5f5f5' }}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36} 
            iconType="circle"
            formatter={(value) => <span className="text-neutral-400 text-sm capitalize">{value.toLowerCase()}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
