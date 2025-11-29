import World from "./Globe";
export default function HomePage () {
    return (
        <>
        <section className="max-w-7xl w-full flex flex-col md:flex-row items-center gap-14">
            
            {/* TEXT LEFT */}
            <div className="flex-1 text-center md:text-left">
              <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold leading-tight mb-4">
                <span className="block">AI-powered real-time</span>
                <span className="block text-blue-400">misinformation detection</span>
                <span className="block">reliability scoring, and crisis insights.</span>
              </h1>

              <p className="text-gray-300 text-md max-w-xl mx-auto md:mx-0">
                MediaSense continuously scans the digital world to detect
                harmful or misleading content before it spreads—giving you
                timely alerts, credibility scores, and crisis-level insights.
              </p>
            </div>

            {/* GLOBE — foreground container */}
            <div className="flex-1 flex justify-center items-center">
              <div className="relative md:-translate-x-1/4">
                <World />
              </div>
            </div>

          </section>
        </>
    );
}