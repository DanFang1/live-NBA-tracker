"use client";

import {
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface Props {
  data: { time: string; pts: number; low: number; high: number }[];
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  const pts = payload.find((p: any) => p.dataKey === "pts");
  const low = payload.find((p: any) => p.dataKey === "low");
  const band = payload.find((p: any) => p.dataKey === "band");
  if (!pts) return null;
  const high = (low?.value ?? 0) + (band?.value ?? 0);
  return (
    <div className="bg-gray-900 border border-gray-700 px-3 py-2 rounded text-sm">
      <p className="text-gray-400">{label}</p>
      <p className="text-green-400">{pts.value} pts</p>
      <p className="text-gray-500">{low?.value?.toFixed(1)} – {high.toFixed(1)} range</p>
    </div>
  );
}

export default function ScoreChart({ data }: Props) {
  if (data.length < 2) return null;

  const chartData = data.map(d => ({
    time: d.time,
    pts: d.pts,
    low: d.low,
    band: +(d.high - d.low).toFixed(1),
  }));

  return (
    <div className="bg-gray-800 rounded-xl p-6 mt-6">
      <p className="text-gray-400 text-sm mb-4">Prediction over time</p>
      <ResponsiveContainer width="100%" height={200}>
        <ComposedChart data={chartData}>
          <XAxis dataKey="time" tick={{ fill: "#9ca3af", fontSize: 11 }} />
          <YAxis domain={["auto", "auto"]} tick={{ fill: "#9ca3af" }} />
          <Tooltip content={<CustomTooltip />} />
          <Area type="monotone" dataKey="low" stroke="none" fill="none" stackId="ci" />
          <Area type="monotone" dataKey="band" stroke="none" fill="#4ade80" fillOpacity={0.15} stackId="ci" />
          <Line type="monotone" dataKey="pts" stroke="#4ade80" strokeWidth={2} dot={false} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
