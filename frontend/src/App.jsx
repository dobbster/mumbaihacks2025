import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import SearchNav from "./components/SearchNav";
import HomePage from "./components/HomePage";
import LiveFeed from "./components/LiveFeed";
import Contributors from "./components/Contributors";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useChatRuntime, AssistantChatTransport } from "@assistant-ui/react-ai-sdk";
import NewsAssistant from "./components/NewsAssistant";

export default function App() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-b from-[#020617] to-[#0a1a3a] text-white">

      {/* Foreground content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        
        {/* NAVBAR */}
            <Navbar />
            <main className="flex-1 flex items-center justify-center px-6 py-12 md:py-20">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/search" element={<SearchNav />} />
                {/* <Route path="/search" element={<NewsAssistant />} /> */}
                <Route path="/live" element={<LiveFeed />} />
                <Route path="/contributors" element={<Contributors />} />
              </Routes>
            </main>

        {/* MAIN HERO SECTION */}
          

        {/* FOOTER */}
        <footer className="text-center p-6 text-gray-400 text-sm">
          © 2025 MediaSense. All rights reserved.
        </footer>

      </div>
    </div>
  );
}
