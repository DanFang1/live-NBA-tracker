"use client";

import { useState, useEffect } from "react";
import ScoreChart from "./components/ScoreChart";


export default function Home() {
  const [players, setPlayers] = useState<{id: number, name: string}[]>([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  const [prediction, setPrediction] = useState<number | null>(null);
  const [ptsLow, setPtsLow] = useState<number | null>(null);
  const [ptsHigh, setPtsHigh] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<{time: string, pts: number, low: number, high: number}[]>([]);

  useEffect(() => {
    fetch("/api/players")
      .then(res => res.json())
      .then(data => setPlayers(data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!selectedPlayerId) return;
    const interval = setInterval(() => {
      fetchPrediction(selectedPlayerId);
    }, 30000);
    return () => clearInterval(interval);
  }, [selectedPlayerId]);

  const selectedPlayerName = players.find(p => p.id === selectedPlayerId)?.name ?? "";

  async function fetchPrediction(playerId: number) {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/live/${playerId}`);
      const data = await res.json();

      if (data.error) {
        setError(data.error);
        setPrediction(null);
        setPtsLow(null);
        setPtsHigh(null);
      } else {
        setPrediction(data.predicted_pts);
        setPtsLow(data.pts_low);
        setPtsHigh(data.pts_high);
        setHistory(prev => [...prev, {
          time: new Date().toLocaleTimeString(),
          pts: data.predicted_pts,
          low: data.pts_low,
          high: data.pts_high,
        }]);
      }
    } catch {
      setError("Could not connect to backend");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-8 text-center">
        Live NBA Props
      </h1>

      <div className="flex gap-3 mb-8">
        <select
          className="flex-1 bg-gray-800 rounded-lg px-4 py-2 text-white"
          value={selectedPlayerId ?? ""}
          onChange={(e) => {
            const id = Number(e.target.value);
            setSelectedPlayerId(id);
            setHistory([]);
            setPtsLow(null);
            setPtsHigh(null);
            fetchPrediction(id);
          }}
        >
          <option value="">Select a player...</option>
          {players.map((player) => (
            <option key={player.id} value={player.id}>{player.name}</option>
          ))}
        </select>
      </div>

      {loading && (
        <p className="text-center text-gray-400">Loading...</p>
      )}

      {error && (
        <p className="text-center text-yellow-400">{error}</p>
      )}

      {prediction !== null && !loading && (
        <div className="bg-gray-800 rounded-xl p-8 text-center">
          <p className="text-gray-400 mb-2">{selectedPlayerName}</p>
          <p className="text-6xl font-bold text-green-400">{prediction}</p>
          <p className="text-gray-400 mt-2">projected points</p>
          {ptsLow !== null && ptsHigh !== null && (
            <p className="text-gray-500 mt-3 text-sm">
              {ptsLow} – {ptsHigh} pts &nbsp;·&nbsp; 80% range
            </p>
          )}
        </div>
      )}

      <ScoreChart data={history} />
    </main>
  );
}
