import Globe from 'react-globe.gl';
import React, { useRef , useState, useEffect } from 'react';
import { csvParse } from "d3-dsv";
const World = () => {
    const [popData, setPopData] = useState([]);
  const globeRef = useRef();
    useEffect(() => {
      // load data
      fetch('./world_population.csv').then(res => res.text())
        .then(csv => csvParse(csv, ({ lat, lng, pop }) => ({ lat: +lat, lng: +lng, pop: +pop })))
        .then(setPopData);
    }, []);

    useEffect(() => {
    let frameId;

    const rotate = () => {
      if (globeRef.current) {
        // Directly rotate THREE.js scene group
        globeRef.current.scene().rotation.y += 0.002;
      }
      frameId = requestAnimationFrame(rotate);
    };

    rotate(); // start loop

    return () => cancelAnimationFrame(frameId);
  }, []);


    return (
    <div  style={{ width: "75%", height: "75%" }}>

      <Globe ref={globeRef}
        globeImageUrl="//cdn.jsdelivr.net/npm/three-globe/example/img/earth-night.jpg"
        heatmapsData={[popData]}
        backgroundColor='rgba(0,0,0,0)'
        heatmapPointLat="lat"
        heatmapPointLng="lng"
        heatmapPointWeight="pop"
        heatmapBandwidth={0.9}
        heatmapColorSaturation={2.8}
        enablePointerInteraction={false}
      />;
    </div>)
  };

export default World;