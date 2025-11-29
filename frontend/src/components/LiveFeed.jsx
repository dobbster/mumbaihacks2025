import { Rss } from "lucide-react";

const dummyRSS = [
  { title: "Breaking News 1", desc: "Short description 1", confidence: 20 },
  { title: "Breaking News 2", desc: "Short description 2", confidence: 85 },
  { title: "Breaking News 3", desc: "Short description 3", confidence: 60 },
  { title: "Breaking News 4", desc: "Short description 4", confidence: 35 },
];

const getConfidenceClasses = (confidence) => {
  if (confidence < 40) return "text-red-400 animate-pulse";
  if (confidence >= 80) return "text-green-400 font-bold";
  return "text-yellow-400";
};

export default function LiveFeed() {
  return (
    <div className="w-full px-10 py-12 text-white">
      
      {/* Title */}
      <div className="flex items-center gap-3 mb-10">
        <h2 className="text-4xl font-bold">Live RSS Feed</h2>
        <Rss className="w-10 h-10 text-orange-400" />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        {dummyRSS.map((item, index) => (
          <div
            key={index}
            className={`
              p-6 rounded-xl border transition
              ${item.confidence >= 80 ? "border-green-500 bg-green-900/20" : "bg-gray-900 border-gray-700"}
              ${item.confidence <= 40 ? "border-red-500" : "bg-gray-900 border-gray-700"}
            `}
          >
            <h3 className="text-xl font-semibold">{item.title}</h3>
            <p className="mt-2 text-gray-300">{item.desc}</p>

            {/* Confidence value */}
            <p className={`mt-4 text-lg ${getConfidenceClasses(item.confidence)}`}>
              Confidence: {item.confidence}%
            </p>
          </div>
        ))}
      </div>

    </div>
  );
}
