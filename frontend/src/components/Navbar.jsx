import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
const { pathname } = useLocation();
const tabClasses = (path) =>
    `cursor-pointer hover:text-blue-300 ${
      pathname === path ? "text-blue-400 underline font-semibold" : ""
    }`;
  return (
    <nav className="w-full px-6 sm:px-8 py-4 flex justify-between items-center bg-black/20 backdrop-blur-md border-b border-gray-800/50 sticky top-0 z-50">
      <div className="text-2xl font-bold">
        <Link to="/" className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent hover:from-blue-300 hover:via-purple-300 hover:to-pink-300 transition-all">
          MediaSense
        </Link>
      </div>

      <div className="flex gap-6 sm:gap-8 text-base sm:text-lg">
        <Link 
          to="/search" 
          className={`${tabClasses("/search")} px-3 py-2 rounded-lg transition-all hover:bg-gray-800/30 ${
            pathname === "/search" ? "bg-gray-800/50" : ""
          }`}
        >
          Search
        </Link>

        {/* LIVE TAB */}
        <Link 
          to="/live" 
          className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all hover:bg-gray-800/30 ${
            pathname === "/live" ? "bg-gray-800/50" : ""
          } ${tabClasses("/live")}`}
        >
          <span>Live</span>
          <span className="relative">
            <span className="w-2 h-2 bg-red-500 rounded-full block"></span>
            <span className="absolute inset-0 w-2 h-2 bg-red-500 rounded-full animate-ping opacity-75"></span>
          </span>
        </Link>

        {/* CONTRIBUTORS TAB */}
        <Link 
          to="/contributors" 
          className={`${tabClasses("/contributors")} px-3 py-2 rounded-lg transition-all hover:bg-gray-800/30 ${
            pathname === "/contributors" ? "bg-gray-800/50" : ""
          }`}
        >
          Contributors
        </Link>
      </div>
    </nav>
  );
}
