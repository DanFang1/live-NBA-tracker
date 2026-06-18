"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface Props {
  data: { time: string; pts: number }[];
}

export default function ScoreChart({ data }: Props) {
  if (data.length < 2) return null;

  return (
    <div className="bg-gray-800 rounded-xl p-6 mt-6">
      <p className="text-gray-400 text-sm mb-4">Prediction over time</p>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <XAxis dataKey="time" tick={{ fill: "#9ca3af", fontSize: 11 }} />
          <YAxis domain={["auto", "auto"]} tick={{ fill: "#9ca3af" }} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="pts"
            stroke="#4ade80"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}