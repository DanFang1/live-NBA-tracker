"use client";

import { useState, useEffect } from "react";

const PLAYER_IDS: Record<string, number> = {
  "LeBron James": 2544,
  "Stephen Curry": 201939,
  "Kevin Durant": 201142,
  "Giannis Antetokounmpo": 203507,
  "Luka Doncic": 1629029,
  "Jayson Tatum": 1628369,
};


export default function Home() {
  const [selectedPlayer, setSelectedPlayer] = useState<string>("");
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<{time: string, pts: number}[]>([]);

  useEffect(() => {
    if (!selectedPlayer) return;
    const interval = setInterval(() => {
      fetchPrediction(selectedPlayer);
    }, 30000);
    return () => clearInterval(interval);
  }, [selectedPlayer]);

  async function fetchPrediction(playerName: string) {
    const playerId = PLAYER_IDS[playerName];
    if (!playerId) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`http://localhost:8000/live/${playerId}`);
      const data = await res.json();

      if (data.error) {
        setError(data.error);
        setPrediction(null);
      } else {
        setPrediction(data.predicted_pts);
        setHistory(prev => [...prev, {
          time: new Date().toLocaleTimeString(),
          pts: data.predicted_pts
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
          value={selectedPlayer}
          onChange={(e) => {
            setSelectedPlayer(e.target.value);
            setHistory([]);
            fetchPrediction(e.target.value);
          }}
        >
          <option value="">Select a player...</option>
          {Object.keys(PLAYER_IDS).map((name) => (
            <option key={name} value={name}>{name}</option>
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
          <p className="text-gray-400 mb-2">{selectedPlayer}</p>
          <p className="text-6xl font-bold text-green-400">{prediction}</p>
          <p className="text-gray-400 mt-2">projected points</p>
        </div>
      )}
    </main>
  );
}