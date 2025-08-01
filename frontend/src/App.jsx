import React, { useEffect, useState } from 'react';
import PitcherCard from './components/PitcherCard';

export default function App() {
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState("");
  const [pitchers, setPitchers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Upload CSV handler
  const handleUpload = async e => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    setUploadMsg("");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        setUploadMsg("Upload successful! Reloading data...");
        setTimeout(() => window.location.reload(), 1200);
      } else {
        setUploadMsg(data.error || "Upload failed.");
      }
    } catch {
      setUploadMsg("Upload failed. Server error.");
    }
    setUploading(false);
  };

  // Fetch pitcher data
  useEffect(() => {
    setLoading(true);
    fetch('https://bullpen-tracker.onrender.com/api/pitchers')
      .then(res => res.json())
      .then(data => {
        setPitchers(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load pitchers.');
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      <h1 className="text-3xl font-bold text-center mt-6 mb-2">Bullpen Usage & Fatigue Tracker</h1>
      <p className="text-center text-sm text-slate-500 mb-4">Monitor pitcher workloads to maximize performance and avoid injuries</p>
      <div className="flex flex-col items-center mb-4">
        <input
          type="text"
          placeholder="Search pitchers..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          className="border border-slate-300 rounded px-2 py-1 w-64 mb-2"
        />
        <div className="flex items-center gap-2">
          <input type="file" accept=".csv" onChange={handleUpload} className="border border-slate-300 rounded px-2 py-1" />
          <button disabled={uploading} className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition">Upload CSV</button>
        </div>
        {uploadMsg && <p className="text-sm text-green-600 mt-2">{uploadMsg}</p>}
      </div>
      {loading ? (
        <p className="text-center text-lg text-slate-400">Loading...</p>
      ) : error ? (
        <p className="text-center text-lg text-red-500">{error}</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-6">
          {pitchers.filter(p => p.name.toLowerCase().includes(searchTerm.toLowerCase())).map(pitcher => (
            <PitcherCard key={pitcher.name} pitcher={pitcher} />
          ))}
        </div>
      )}
    </div>
  );
}
