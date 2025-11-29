import { Rss } from "lucide-react";

const dummyRSS = [
  { title: "Russian President Vladimir Putin to visit India on December 4-5 for annual summit", desc: "The Ministry of External Affairs on Friday announced that Putin will visit India on December 4 and 5. The visit aims to strengthen India-Russia ties and discuss key regional and global issues.", confidence: 20 },
  { title: "Wedding choreographer issues statement amid Smriti Mandhana–Palaash Muchhal 'cheating' controversy", desc: "After much speculation surrounding the wedding of Smriti Mandhana and Palaash Muchhal, one of the choreographers has issued a clarification", confidence: 85 },
  { title: "'India will be completely free of Naxalism': Amit Shah's bold remark, sets deadline", desc: "\"A 360-degree attack has to be launched against narcotics and organised crime,\" Amit Shah said in Raipur.", confidence: 60 },
  { title: "RBI Imposes Rs 91 Lakh Fine On HDFC Bank For Violations Including KYC Lapses", desc: "The penalty has been imposed on the private sector lender for deficiencies in statutory and regulatory compliance, including those related to Know Your Customer (KYC).", confidence: 35 },
];

const getConfidenceConfig = (confidence) => {
  if (confidence >= 80) {
    return {
      color: "text-red-400",
      bgGradient: "from-red-900/30 to-red-800/20",
      borderColor: "border-red-500/50",
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      ),
      label: "High Risk",
      pulse: true
    };
  }
  if (confidence <= 40) {
    return {
      color: "text-green-400",
      bgGradient: "from-green-900/30 to-emerald-800/20",
      borderColor: "border-green-500/50",
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      ),
      label: "Legitimate",
      pulse: false
    };
  }
  return {
    color: "text-yellow-400",
    bgGradient: "from-yellow-900/30 to-amber-800/20",
    borderColor: "border-yellow-500/50",
    icon: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
      </svg>
    ),
    label: "Uncertain",
    pulse: false
  };
};

export default function LiveFeed() {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 text-white">
      
      {/* Header Section */}
      <div className="mb-10 sm:mb-12">
        <div className="flex items-center gap-4 mb-4">
          <div className="relative">
            <Rss className="w-10 h-10 sm:w-12 sm:h-12 text-orange-400" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
          </div>
          <div>
            <h2 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-orange-400 to-pink-400 bg-clip-text text-transparent">
              Live RSS Feed
            </h2>
            <p className="text-gray-400 text-sm sm:text-base mt-1">Real-time misinformation detection updates</p>
          </div>
        </div>
        
        {/* Stats Bar */}
        <div className="flex flex-wrap gap-4 mt-6">
          <div className="px-4 py-2 bg-gray-800/50 rounded-lg border border-gray-700/50 backdrop-blur-sm">
            <span className="text-gray-400 text-sm">Total Items:</span>
            <span className="ml-2 text-white font-semibold">{dummyRSS.length}</span>
          </div>
          <div className="px-4 py-2 bg-red-900/30 rounded-lg border border-red-700/50 backdrop-blur-sm">
            <span className="text-red-400 text-sm">High Risk:</span>
            <span className="ml-2 text-red-300 font-semibold">
              {dummyRSS.filter(item => item.confidence >= 80).length}
            </span>
          </div>
          <div className="px-4 py-2 bg-green-900/30 rounded-lg border border-green-700/50 backdrop-blur-sm">
            <span className="text-green-400 text-sm">Legitimate:</span>
            <span className="ml-2 text-green-300 font-semibold">
              {dummyRSS.filter(item => item.confidence <= 40).length}
            </span>
          </div>
        </div>
      </div>

      {/* Feed Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {dummyRSS.map((item, index) => {
          const config = getConfidenceConfig(item.confidence);
          return (
            <div
              key={index}
              className={`
                group relative bg-gradient-to-br ${config.bgGradient} backdrop-blur-xl
                border ${config.borderColor} rounded-2xl shadow-2xl
                p-6 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl
                animate-fadeIn
                ${config.pulse ? 'animate-pulse' : ''}
              `}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Status Badge */}
              <div className="absolute top-4 right-4 z-10">
                <div className={`
                  flex items-center gap-1.5 px-3 py-1.5 rounded-full
                  bg-gray-900/50 backdrop-blur-sm border ${config.borderColor}
                  ${config.color} whitespace-nowrap
                `}>
                  {config.icon}
                  <span className="text-xs font-semibold">{config.label}</span>
                </div>
              </div>

              {/* Content */}
              <div className="pr-28 sm:pr-32">
                <div className="relative group/title mb-3">
                  <h3 
                    className="text-lg font-bold text-white line-clamp-2 leading-snug pr-2 cursor-help"
                  >
                    {item.title}
                  </h3>
                  {/* Custom Tooltip */}
                  <div className="absolute left-0 bottom-full mb-2 w-72 p-3 bg-gray-900/95 backdrop-blur-sm text-white text-sm rounded-lg shadow-2xl border border-gray-700 opacity-0 invisible group-hover/title:opacity-100 group-hover/title:visible transition-all duration-200 z-30 pointer-events-none transform translate-y-1 group-hover/title:translate-y-0">
                    <div className="font-semibold mb-1">{item.title}</div>
                    <div className="absolute -bottom-1 left-6 w-2 h-2 bg-gray-900 border-r border-b border-gray-700 transform rotate-45"></div>
                  </div>
                </div>
                <div className="relative group/desc">
                  <p 
                    className="text-sm text-gray-300 line-clamp-3 leading-relaxed cursor-help"
                  >
                    {item.desc}
                  </p>
                  {/* Custom Tooltip */}
                  <div className="absolute left-0 bottom-full mb-2 w-80 p-3 bg-gray-900/95 backdrop-blur-sm text-white text-sm rounded-lg shadow-2xl border border-gray-700 opacity-0 invisible group-hover/desc:opacity-100 group-hover/desc:visible transition-all duration-200 z-30 pointer-events-none transform translate-y-1 group-hover/desc:translate-y-0">
                    <div>{item.desc}</div>
                    <div className="absolute -bottom-1 left-6 w-2 h-2 bg-gray-900 border-r border-b border-gray-700 transform rotate-45"></div>
                  </div>
                </div>
              </div>

              {/* Confidence Meter */}
              <div className="mt-6 pt-4 border-t border-gray-700/50">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400 font-medium">Confidence Score</span>
                  <span className={`text-sm font-bold ${config.color}`}>
                    {item.confidence}%
                  </span>
                </div>
                
                {/* Progress Bar */}
                <div className="w-full h-2 bg-gray-800/50 rounded-full overflow-hidden">
                  <div
                    className={`
                      h-full rounded-full transition-all duration-500
                      ${item.confidence >= 80 
                        ? 'bg-gradient-to-r from-red-500 to-red-600' 
                        : item.confidence <= 40
                        ? 'bg-gradient-to-r from-green-500 to-emerald-600'
                        : 'bg-gradient-to-r from-yellow-500 to-amber-600'
                      }
                    `}
                    style={{ width: `${item.confidence}%` }}
                  ></div>
                </div>
              </div>

              {/* Hover Effect Indicator */}
              <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <div className={`absolute inset-0 rounded-2xl ${config.borderColor.replace('border-', 'ring-2 ring-')} ring-opacity-50`}></div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty State (if needed) */}
      {dummyRSS.length === 0 && (
        <div className="text-center py-16">
          <Rss className="w-16 h-16 mx-auto text-gray-600 mb-4" />
          <p className="text-gray-400 text-lg">No feed items available at the moment</p>
        </div>
      )}

    </div>
  );
}
