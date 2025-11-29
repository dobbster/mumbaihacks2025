import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
const { pathname } = useLocation();
const tabClasses = (path) =>
    `cursor-pointer hover:text-blue-300 ${
      pathname === path ? "text-blue-400 underline font-semibold" : ""
    }`;
  return (
    <nav className="w-full px-8 py-4 flex justify-between items-center bg-black/30 backdrop-blur">
      <div className="text-2xl font-bold text-white-400">
        <Link to="/">
          MediaSense
        </Link>
      </div>

      <div className="flex gap-8 text-lg">
        <Link to="/search" className={tabClasses("/search")}>
          Search
        </Link>

        {/* LIVE TAB */}
        <Link to="/live" className={`flex items-center gap-2 ${tabClasses("/live")}`}>
          <span>Live</span>
          <span className="w-2 h-2 bg-red-500 rounded-full animate-ping"></span>
        </Link>

        {/* CONTRIBUTORS TAB */}
        <Link to="/contributors" className={tabClasses("/contributors")}>
          Contributors
        </Link>
      </div>
    </nav>
  );
}
