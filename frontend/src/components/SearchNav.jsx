import React, { useState } from "react";

export default function SearchNav() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");

  const handleVerify = () => {
    if (!query.trim()) {
      setResult("Please enter something to verify.");
      return;
    }
    setResult(`You searched for: ${query}`);
  };

  return (
    <section className="max-w-7xl w-full flex flex-col md:flex-row items-center gap-14">
        <div className="w-full bg-gray-900 text-white p-4 shadow-lg">
        <h1 className="text-l font-semibold">Information Search</h1>
        <div className="mt-4 p-4 bg-gray-800 rounded-lg animate-fadeIn">
        <div className="flex gap-3">
            <input
            type="text"
            placeholder="Enter text..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 px-3 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none"
            />

            <button
            onClick={handleVerify}
            className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-700 transition"
            >
            Verify
            </button>
        </div>

        {/* Result Container */}
        <div className="mt-3 p-3 bg-gray-700 rounded-lg text-sm text-gray-200">
            {result || "Result will appear here."}
        </div>
        </div>
        </div>
    </section>
  );
}
