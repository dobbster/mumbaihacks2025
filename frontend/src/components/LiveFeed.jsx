import { Rss } from "lucide-react";

const dummyRSS = [
  { title: "Russian President Vladimir Putin to visit India on December 4-5 for annual summit", desc: "The Ministry of External Affairs on Friday announced that Putin will visit India on December 4 and 5. The visit aims to strengthen India-Russia ties and discuss key regional and global issues.", confidence: 20 },
  { title: "Wedding choreographer issues statement amid Smriti Mandhana–Palaash Muchhal ‘cheating’ controversy", desc: "After much speculation surrounding the wedding of Smriti Mandhana and Palaash Muchhal, one of the choreographers has issued a clarification", confidence: 85 },
  { title: "‘India will be completely free of Naxalism’: Amit Shah's bold remark, sets deadline", desc: "“A 360-degree attack has to be launched against narcotics and organised crime,” Amit Shah said in Raipur.", confidence: 60 },
  { title: "RBI Imposes Rs 91 Lakh Fine On HDFC Bank For Violations Including KYC Lapses", desc: "The penalty has been imposed on the private sector lender for deficiencies in statutory and regulatory compliance, including those related to Know Your Customer (KYC).", confidence: 35 },
];

const getConfidenceClasses = (confidence) => {
  if (confidence >= 80) return "text-red-400 animate-pulse";
  if (confidence <= 40) return "text-green-400 font-bold";
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
              ${item.confidence <= 40 ? "border-green-500 bg-green-900/20" : "bg-gray-900 border-gray-700"}
              ${item.confidence >= 80 ? "border-red-500" : "bg-gray-900 border-gray-700"}
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
