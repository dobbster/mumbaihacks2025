import React, { useState } from "react";

export default function SearchNav() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");

  const getStatusColor = (status) => {
  if (!status) return "text-gray-300";

  if (status.toLowerCase() === "misinformation") return "text-red-400";
  if (status.toLowerCase() === "uncertain") return "text-yellow-400";
  if (status.toLowerCase() === "legitimate") return "text-green-400";

  return "text-gray-300"; // fallback
};

const handleClear = () => {
  setQuery("");
  setResult(null);
};

const mockData = {
  "status": "success",
  "prompt": "Are seawater levels rising around the world?",
  "queries": [
    "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
    "site:ndtv.com Are seawater levels rising around the world?",
    "site:thehindu.com Are seawater levels rising around the world?",
    "site:indianexpress.com Are seawater levels rising around the world?",
    "site:hindustantimes.com Are seawater levels rising around the world?",
    "site:livemint.com Are seawater levels rising around the world?",
    "site:business-standard.com Are seawater levels rising around the world?",
    "site:news18.com Are seawater levels rising around the world?",
    "site:scroll.in Are seawater levels rising around the world?",
    "site:deccanherald.com Are seawater levels rising around the world?"
  ],
  "results": [
    {
      "id": "tavily_91feb6ef",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea levels are rising faster than in 4000 years",
      "content": "Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate change and melting ice. Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate change and melting ice. These data help researchers predict future trends, assess climate change impacts, and develop adaptive strategies for vulnerable coastal communities facing rising seas and increased flooding risks.Research by Rutgers University has reconstructed sea level patterns spanning almost 12,000 years, tracing back to the Holocene epoch, which began around 11,700 years ago after the last major ice age.",
      "url": "https://timesofindia.indiatimes.com/etimes/trending/sea-levels-are-rising-faster-than-in-4000-years-hidden-threats-to-cities-causes-and-impacts/articleshow/124722208.cms",
      "published_at": "2025-11-29T02:11:00.177988Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.6824261,
      "ingested_at": "2025-11-29T02:11:00.178009Z"
    },
    {
      "id": "tavily_8490d888",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea level rise getting faster, finds new study",
      "content": "Environment News: Global sea levels are rising significantly faster than earlier thought, according to a new Harvard study.",
      "url": "https://timesofindia.indiatimes.com/home/environment/global-warming/Sea-level-rise-getting-faster-finds-new-study/articleshow/45899326.cms",
      "published_at": "2025-11-29T02:11:00.178024Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.61168414,
      "ingested_at": "2025-11-29T02:11:00.178029Z"
    },
    {
      "id": "tavily_11ea30de",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Nasa study shows interplay of El Niño and La Niña cycles ...",
      "content": "New data indicates that global sea levels are rising at an accelerating rate, posing an increased threat of flooding and coastal erosion. Recent",
      "url": "https://timesofindia.indiatimes.com/science/nasa-study-shows-interplay-of-el-nio-and-la-nia-cycles-impacts-global-sea-levels/articleshow/110935630.cms",
      "published_at": "2025-11-29T02:11:00.178037Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.6108487,
      "ingested_at": "2025-11-29T02:11:00.178041Z"
    },
    {
      "id": "tavily_50a68002",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Arabian Sea may rise by nearly 3ft over greenhouse effect",
      "content": "Global sea levels are rising because of human-caused global warming, with recent rates being unprecedented over the past 2,500-plus years.",
      "url": "https://timesofindia.indiatimes.com/city/pune/arabian-sea-may-rise-by-nearly-3ft-over-greenhouse-effect/articleshow/103562742.cms",
      "published_at": "2025-11-29T02:11:00.178048Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.5993685,
      "ingested_at": "2025-11-29T02:11:00.178052Z"
    },
    {
      "id": "tavily_bbf1b89b",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Global sea level surging at faster rate: Study",
      "content": "WASHINGTON: The global sea level is not rising at a steady rate, it is accelerating a little every year, according to a new assessment based on 25 years of",
      "url": "https://timesofindia.indiatimes.com/home/environment/global-warming/global-sea-level-surging-at-faster-rate-study/articleshow/62899291.cms",
      "published_at": "2025-11-29T02:11:00.178059Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.5914643,
      "ingested_at": "2025-11-29T02:11:00.178062Z"
    },
    {
      "id": "tavily_c381b085",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Antarctica Sees Similar Climate Change Effects As ...",
      "content": "home     World News     Antarctica Sees Similar Climate Change Effects As Greenland: Study ## If Greenland's ice sheet were to melt entirely, global sea levels would rise by about seven metres (23 feet). If this were to occur in Antarctica, the sea level rise could exceed 50 metres. The planet's warming climate is having effects in Antarctica that increasingly resemble those observed in the Arctic, meaning global sea levels could rise faster that previously predicted, Danish researchers warned on Friday. If this were to occur in Antarctica, the sea level rise could exceed 50 metres, DMI said. Track Latest News Live on NDTV.com and get news updates from India  and around the world",
      "url": "https://www.ndtv.com/world-news/antarctica-sees-similar-climate-change-effects-as-greenland-study-9389880",
      "published_at": "2025-11-29T02:11:00.839115Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:ndtv.com Are seawater levels rising around the world?",
      "relevance_score": 0.6844544,
      "ingested_at": "2025-11-29T02:11:00.839134Z"
    },
    {
      "id": "tavily_e1468092",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea Level Will Rise by 1 Meter, It's Unavoidable: NASA",
      "content": "Sea levels are rising around the world, and the latest satellite data suggests that three feet (one meter) or more is unavoidable in the",
      "url": "https://www.ndtv.com/world-news/nasa-sees-unavoidable-sea-level-rise-ahead-1211395",
      "published_at": "2025-11-29T02:11:00.839144Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:ndtv.com Are seawater levels rising around the world?",
      "relevance_score": 0.6824261,
      "ingested_at": "2025-11-29T02:11:00.839148Z"
    },
    {
      "id": "tavily_3d81a31d",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Video: NASA Tracks 30 Years of Sea Level Rise In A New ...",
      "content": "Global average sea levels have risen faster since 1900. The Average sea level around the globe is increasing as the planet Earth warms and ...See more",
      "url": "https://www.ndtv.com/feature/video-nasa-tracks-30-years-of-sea-level-rise-in-a-new-terrifying-animation-4140432",
      "published_at": "2025-11-29T02:11:00.839154Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:ndtv.com Are seawater levels rising around the world?",
      "relevance_score": 0.53225553,
      "ingested_at": "2025-11-29T02:11:00.839157Z"
    },
    {
      "id": "tavily_e1413efa",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Rise in Sea Level Doubled in Three Decades, Say ...",
      "content": "The rise of sea level in the world is around three millimetres per year, which is double the rate three decades ago, a senior scientist said",
      "url": "https://www.ndtv.com/goa-news/rise-in-sea-level-doubled-in-three-decades-say-researchers-575644",
      "published_at": "2025-11-29T02:11:00.839163Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:ndtv.com Are seawater levels rising around the world?",
      "relevance_score": 0.502564,
      "ingested_at": "2025-11-29T02:11:00.839167Z"
    },
    {
      "id": "tavily_15de172b",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea Levels Rise",
      "content": "Over 100 Million Buildings Worldwide Could Face Flooding Risk From Rising Seas, Study Warns.",
      "url": "https://www.ndtv.com/topic/sea-levels-rise",
      "published_at": "2025-11-29T02:11:00.839172Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:ndtv.com Are seawater levels rising around the world?",
      "relevance_score": 0.45318982,
      "ingested_at": "2025-11-29T02:11:00.839176Z"
    },
    {
      "id": "tavily_8a163ba7",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Explained | How rising sea levels threaten agriculture, ...",
      "content": "According to the WMO report, the sea level has been rising in the three decades for which satellite altimeter data is available (1993-2022). Nehru Prabakaran, a scientist at the Wildlife Institute of India (WII), Dehradun, who works on the effect of sea-level change on coastal ecosystems, told *The Hindu* that the WMO report confirms trends that are already well-known. For example, he said that in the Sunderbans delta in West Bengal, the world’s largest mangrove area, rising sea levels and coastal erosion, due to loss of land and sediment from coastal areas, has left more islands submerged under water, and that in turn has forced members of local communities to migrate.",
      "url": "https://www.thehindu.com/sci-tech/energy-and-environment/rising-sea-levels-threaten-agriculture-rainfall-social-fabric/article66781156.ece",
      "published_at": "2025-11-29T02:11:01.508263Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:thehindu.com Are seawater levels rising around the world?",
      "relevance_score": 0.72629017,
      "ingested_at": "2025-11-29T02:11:01.508278Z"
    },
    {
      "id": "tavily_114b0ab4",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea levels around Indian coastlines projected to rise up ...",
      "content": "According to the latest IPCC Sixth Assessment Report, the global mean sea level has been rising over the last century at a rate of 1.8 mm/year.",
      "url": "https://www.thehindu.com/news/national/telangana/sea-levels-around-indian-coastlines-projected-to-rise-up-to-1-metre-by-2100-incois-study/article70303156.ece",
      "published_at": "2025-11-29T02:11:01.508285Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:thehindu.com Are seawater levels rising around the world?",
      "relevance_score": 0.56661874,
      "ingested_at": "2025-11-29T02:11:01.508288Z"
    },
    {
      "id": "tavily_6c8e05a9",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea level rise cannot be pumped away - Frontline - The Hindu",
      "content": "Under unabated warming, sea level rise may exceed 130 cm by 2100. Climate scientists at the Potsdam Institute for Climate Impact (PIK), Germany,",
      "url": "https://frontline.thehindu.com/science-and-technology/sea-level-rise-cannot-be-pumped-away/article8466317.ece",
      "published_at": "2025-11-29T02:11:01.508293Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:thehindu.com Are seawater levels rising around the world?",
      "relevance_score": 0.48074743,
      "ingested_at": "2025-11-29T02:11:01.508296Z"
    },
    {
      "id": "tavily_daa1c139",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "As oceans rise, are some nations doomed to vanish?",
      "content": "India   World   Movies   Sport   Data   Health   Opinion   Science   Business   Premium The prospect is no longer science fiction as global warming gathers pace, posing an unprecedented challenge to the international community, and threatening entire peoples with the loss of their land and identity. This is still below the highest point of the smallest, flattest island states, but rising seas will be accompanied by an increase in storms and tidal surges: Salt contamination to water and land will make many atolls uninhabitable long before they are covered over by the sea. In an August 2021 declaration, the members of the Pacific Islands Forum, including Australia and New Zealand, proclaimed that their maritime zones \"shall continue to apply, without reduction, notwithstanding any physical changes connected to climate change-related sea level rise.\"",
      "url": "https://www.thehindu.com/sci-tech/energy-and-environment/as-oceans-rise-are-some-nations-doomed-to-vanish/article65991818.ece",
      "published_at": "2025-11-29T02:11:01.508300Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:thehindu.com Are seawater levels rising around the world?",
      "relevance_score": 0.39459804,
      "ingested_at": "2025-11-29T02:11:01.508302Z"
    },
    {
      "id": "tavily_657dc7ef",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Data show seas rising faster around Maldives ...",
      "content": "September 1, 2025e-Paper Account Opinion   Editorial   Cartoon   Columns   Comment   Interview   Lead   Letters   Open Page   Corrections & Clarifications Education Education   Careers   Colleges   Schools September 1, 2025e-Paper Published - September 01, 2025 05:15 am IST Published - September 01, 2025 05:15 am IST * Access to comment on every story ### Comments Comments have to be in English, and in full sentences. Please abide by our community guidelines  for posting your comments. We have migrated to a new commenting platform. If you are already a registered user of The Hindu and logged in, you may continue to engage with our articles. If you do not have an account please register and login to post comments. Users can access their older comments by logging into their accounts on Vuukle.",
      "url": "https://www.thehindu.com/sci-tech/science/data-show-seas-rising-faster-around-maldives-lakshadweep-than-believed/article69996142.ece",
      "published_at": "2025-11-29T02:11:01.508307Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:thehindu.com Are seawater levels rising around the world?",
      "relevance_score": 0.38706517,
      "ingested_at": "2025-11-29T02:11:01.508309Z"
    },
    {
      "id": "tavily_a9589aea",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Almost 2 cm of sea level rise this century was due to ...",
      "content": "## Coastal cities in India have also witnessed the sea level rise in recent years. For instance, the southwestern Indian Ocean region is seeing the sea level rise at a rate of 2.5 mm per year, faster than the global average, according to a 2022 World Meteorological Organization report. Coastal cities in India have also witnessed the sea level rise in recent years. In a 2024 statement, Nadya Vinogradova Shiffer, director of the NASA sea level change team and the ocean physics program in Washington, said, “Current rates of acceleration mean that we are on track to add another 20 cm of global mean sea level by 2050, doubling the amount of change in the next three decades compared to the previous 100 years and increasing the frequency and impacts of floods across the world.”",
      "url": "https://indianexpress.com/article/explained/explained-climate/melting-glaciers-2-cm-sea-level-rise-9849231/",
      "published_at": "2025-11-29T02:11:02.183452Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
      "relevance_score": 0.5582553,
      "ingested_at": "2025-11-29T02:11:02.183468Z"
    },
    {
      "id": "tavily_940c6c2e",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "36 million Indians may face annual floods by 2050 due to ...",
      "content": "It had showed that while sea level rose globally around 15 cm during the 20th century, it is currently rising at more than twice the speed — 3. ...See more",
      "url": "https://indianexpress.com/article/india/36-million-indians-may-face-annual-floods-by-2050-due-to-sea-level-rise-study-6093630/",
      "published_at": "2025-11-29T02:11:02.183478Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
      "relevance_score": 0.5510187,
      "ingested_at": "2025-11-29T02:11:02.183481Z"
    },
    {
      "id": "tavily_aa380693",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Mumbai, Dhaka, London, New York among metros in line ...",
      "content": "India, China, Bangladesh and the Netherlands face the highest threat of sea-level rise globally, according to a new report by the World Meteorological ...See more",
      "url": "https://indianexpress.com/article/india/mumbai-dhaka-london-new-york-among-metros-in-line-of-sea-level-rise-threat-report-8445371/",
      "published_at": "2025-11-29T02:11:02.183487Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
      "relevance_score": 0.529337,
      "ingested_at": "2025-11-29T02:11:02.183490Z"
    },
    {
      "id": "tavily_047e7430",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "World's mangroves, marshes & coral could be devastated ...",
      "content": "A similar rise in sea levels could happen due to human-caused global warming today, devastating coastal agriculture around the world.",
      "url": "https://indianexpress.com/article/technology/science/world-mangrove-marshes-coral-sea-level-rise-8925444/",
      "published_at": "2025-11-29T02:11:02.183495Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
      "relevance_score": 0.5065188,
      "ingested_at": "2025-11-29T02:11:02.183498Z"
    },
    {
      "id": "tavily_d0a61639",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Digging Deep: Deltas losing land due to rising sea levels ...",
      "content": "Rising sea levels and human intervention in rivers are rapidly changing river-dynamics across the world. Read more below in today's edition",
      "url": "https://indianexpress.com/article/technology/science/digging-deep-deltas-losing-land-due-to-rising-sea-levels-and-rivers-changing-course-8086106/",
      "published_at": "2025-11-29T02:11:02.183503Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
      "relevance_score": 0.47957736,
      "ingested_at": "2025-11-29T02:11:02.183506Z"
    },
    {
      "id": "tavily_2e120501",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea-levels could rise up to 4 ft by end of century due ...",
      "content": "Sea-levels could rise up to 4 ft by end of century due to global warming, warn scientists | Hindustan Times.",
      "url": "https://www.hindustantimes.com/science/sea-levels-could-rise-up-to-4-ft-by-end-of-century-due-to-global-warming-warn-scientists/story-LtFEGbRBkXnAXExYeaKINN.html",
      "published_at": "2025-11-29T02:11:02.904084Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.6862234,
      "ingested_at": "2025-11-29T02:11:02.904105Z"
    },
    {
      "id": "tavily_c0bca29c",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Global warming is destroying Costa Rica's coastline, ...",
      "content": "Global warming could cause sea levels around the world to rise between 70 cm and 1.2 metres (28-47 inches) in the next two centuries, ramping",
      "url": "https://www.hindustantimes.com/travel/how-global-warming-is-destroying-costa-rica-s-coastline-threatening-tourism/story-3AA3tgLpRpRqFkMEMfmcSP.html",
      "published_at": "2025-11-29T02:11:02.904115Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.5911811,
      "ingested_at": "2025-11-29T02:11:02.904119Z"
    },
    {
      "id": "tavily_08cd133f",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "NASA visualises how sea levels will rise in Indian coastal ...",
      "content": "Global mean sea level increased by 0.20m between 1901 and 2018. Sea level around Asia in the North Indian Ocean has increased faster than",
      "url": "https://www.hindustantimes.com/environment/nasa-visualises-how-sea-levels-will-rise-in-indian-coastal-regions-101629257135231.html",
      "published_at": "2025-11-29T02:11:02.904126Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.5462305,
      "ingested_at": "2025-11-29T02:11:02.904130Z"
    },
    {
      "id": "tavily_cbcc5029",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea-level rise a major threat to India, other nations: WMO",
      "content": "Global mean sea-level increased by 0.20m between 1901 and 2018, with an average rate increase of 1.3 mm/ year between 1901 and 1971,1.9 mm/year",
      "url": "https://www.hindustantimes.com/india-news/sealevel-rise-a-major-threat-to-india-other-nations-wmo-101676400422024.html",
      "published_at": "2025-11-29T02:11:02.904136Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.52583206,
      "ingested_at": "2025-11-29T02:11:02.904139Z"
    },
    {
      "id": "tavily_317242e2",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "It's time for Northeast to prep for floods like those that hit ...",
      "content": "Worldwide, sea levels have risen faster since 1900, putting hundreds of millions of people at risk, the United Nations has said.",
      "url": "https://www.hindustantimes.com/world-news/its-time-for-northeast-to-prep-for-floods-like-those-that-hit-this-winter-climate-change-is-why-101707973890571.html",
      "published_at": "2025-11-29T02:11:02.904146Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
      "relevance_score": 0.5150107,
      "ingested_at": "2025-11-29T02:11:02.904149Z"
    },
    {
      "id": "tavily_b30ced11",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Global sea level surging at faster rate, says study - Mint",
      "content": "Washington: The global sea level is not rising at a steady rate, it is accelerating a little every year, according to a new assessment based",
      "url": "https://www.livemint.com/Science/OP5KylsYDrsFtx64xlHEqK/Global-sea-level-surging-at-faster-rate-says-study.html",
      "published_at": "2025-11-29T02:11:03.556232Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:livemint.com Are seawater levels rising around the world?",
      "relevance_score": 0.7092009,
      "ingested_at": "2025-11-29T02:11:03.556240Z"
    },
    {
      "id": "tavily_83a9a54b",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea levels rising faster than predicted: Nasa scientists - Mint",
      "content": "The world's oceans have risen an average of almost 3 inches since 1992, due to global warming, say Nasa researchers.",
      "url": "https://www.livemint.com/Politics/VHt3v3xOaL9Wytkp5WkbvO/Warming-seas-rising-faster-than-predicted-Nasa.html",
      "published_at": "2025-11-29T02:11:03.556244Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:livemint.com Are seawater levels rising around the world?",
      "relevance_score": 0.70750624,
      "ingested_at": "2025-11-29T02:11:03.556245Z"
    },
    {
      "id": "tavily_ca02a456",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "In Hot Water - Mint",
      "content": "And if atmospheric temperatures are rising around the world, it is because the ocean is nearly saturated with an unnatural amount of heat.",
      "url": "https://livemint.com/mint-top-newsletter/climate-change12122024.html",
      "published_at": "2025-11-29T02:11:03.556247Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:livemint.com Are seawater levels rising around the world?",
      "relevance_score": 0.6426349,
      "ingested_at": "2025-11-29T02:11:03.556249Z"
    },
    {
      "id": "tavily_cc5d7c6a",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Rising sea levels may sink Mumbai by 2100: IPCC report - Mint",
      "content": "Global sea levels are set to rise by at least 1m by 2100 if carbon emissions go unchecked, submerging hundreds of cities, including Mumbai and Kolkata.",
      "url": "https://www.livemint.com/news/india/rising-sea-levels-may-sink-mumbai-by-2100-ipcc-report-1569436019802.html",
      "published_at": "2025-11-29T02:11:03.556251Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:livemint.com Are seawater levels rising around the world?",
      "relevance_score": 0.6391287,
      "ingested_at": "2025-11-29T02:11:03.556252Z"
    },
    {
      "id": "tavily_f7bbca16",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Ocean warming has almost doubled in the last decade: Study",
      "content": "“The world ocean, in 2023, is now the hottest ever recorded, and sea levels are rising because heat causes water to expand and ice to melt,”",
      "url": "https://www.livemint.com/mint-lounge/business-of-life/ocean-warming-doubled-greenhouse-gas-111699013336640.html",
      "published_at": "2025-11-29T02:11:03.556254Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:livemint.com Are seawater levels rising around the world?",
      "relevance_score": 0.62879556,
      "ingested_at": "2025-11-29T02:11:03.556255Z"
    },
    {
      "id": "tavily_570ca3c2",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Global sea levels may rise by 2300 if greenhouse gas ...",
      "content": "From 2000 to 2050, global average sea-level will most likely rise about 6 to 10 inches, but is extremely unlikely to rise by more than 18 inches",
      "url": "https://www.business-standard.com/article/current-affairs/global-sea-levels-may-rise-by-2300-if-greenhouse-gas-emissions-remain-high-118100800453_1.html",
      "published_at": "2025-11-29T02:11:04.216191Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:business-standard.com Are seawater levels rising around the world?",
      "relevance_score": 0.53094244,
      "ingested_at": "2025-11-29T02:11:04.216210Z"
    },
    {
      "id": "tavily_504e5ee4",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Rising seas 'worldwide catastrophe' affecting Pacific ...",
      "content": "Globally, sea level rise has been accelerating, the UN report said, echoing peer-reviewed studies. The rate is now the fastest it has been in 3",
      "url": "https://www.business-standard.com/world-news/rising-seas-worldwide-catastrophe-affecting-pacific-paradises-un-chief-124082700056_1.html",
      "published_at": "2025-11-29T02:11:04.216219Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:business-standard.com Are seawater levels rising around the world?",
      "relevance_score": 0.45289946,
      "ingested_at": "2025-11-29T02:11:04.216222Z"
    },
    {
      "id": "tavily_6f96b56a",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Global sea levels could rise 2m by the end of century, finds ...",
      "content": "Global sea levels could rise by two metres (6.5 feet) and displace tens of millions of people by the end of the century, according to new",
      "url": "https://www.business-standard.com/article/pti-stories/2-metre-sea-level-rise-plausible-by-2100-study-119052101264_1.html",
      "published_at": "2025-11-29T02:11:04.216228Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:business-standard.com Are seawater levels rising around the world?",
      "relevance_score": 0.4292146,
      "ingested_at": "2025-11-29T02:11:04.216231Z"
    },
    {
      "id": "tavily_f7ab5260",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea levels to rise 10-12 inches by 2050, rate alarming",
      "content": "Sea levels along US coastlines will rise between 10 to 12 inches (25 to 30 cm) on average above the current levels by 2050, according to a",
      "url": "https://www.business-standard.com/article/international/sea-levels-to-rise-10-12-inches-by-2050-rate-alarming-report-122021700192_1.html",
      "published_at": "2025-11-29T02:11:04.216236Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:business-standard.com Are seawater levels rising around the world?",
      "relevance_score": 0.41648865,
      "ingested_at": "2025-11-29T02:11:04.216239Z"
    },
    {
      "id": "tavily_945e5a17",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Glaciers Are Melting But Antarctica's Sea Levels ...",
      "content": "# Glaciers Are Melting But Antarctica’s Sea Levels Are Falling Instead Of Rising. Antarctica's ice melt lowers local sea levels due to reduced gravity but raises global levels. This dramatic reversal is considered one of the most remarkable natural processes, and a new study has revealed a surprising twist: as Antarctica’s ice melts, global sea levels will rise, yet the sea level around Antarctica itself will actually fall. As a result, sea levels fall close to Antarctica, while rising rapidly across the rest of the world. 1. **Isostatic rebound:** As ice mass reduces, the land beneath Antarctica slowly rises, lifting some ice away from warm ocean waters and slowing melting. News world  Glaciers Are Melting But Antarctica’s Sea Levels Are Falling Instead Of Rising.",
      "url": "https://www.news18.com/world/glaciers-are-melting-but-antarcticas-sea-levels-are-falling-instead-of-rising-heres-why-ws-akl-9737211.html",
      "published_at": "2025-11-29T02:11:05.023259Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:news18.com Are seawater levels rising around the world?",
      "relevance_score": 0.6407488,
      "ingested_at": "2025-11-29T02:11:05.023274Z"
    },
    {
      "id": "tavily_0caedd81",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "World Oceans Day 2022: Do You Know These Cool Facts ...",
      "content": "Rising sea levels, more frequent powerful storms, plastic pollution and much more has threatened the health of oceans.",
      "url": "https://www.news18.com/news/lifestyle/world-oceans-day-2022-do-you-know-these-cool-facts-about-oceans-5326231.html",
      "published_at": "2025-11-29T02:11:05.023284Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:news18.com Are seawater levels rising around the world?",
      "relevance_score": 0.4654124,
      "ingested_at": "2025-11-29T02:11:05.023289Z"
    },
    {
      "id": "tavily_93f8b86b",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Melting Atlantic Glacier Will Increase Sea-level by 20 ...",
      "content": "Global warming is causing our glaciers to melt faster and our sea level is rising by an alarming global average of 3.3 millimetres per year",
      "url": "https://www.news18.com/news/buzz/melting-atlantic-glacier-will-increase-sea-level-by-20-percent-more-than-previously-predicted-3706526.html",
      "published_at": "2025-11-29T02:11:05.023295Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:news18.com Are seawater levels rising around the world?",
      "relevance_score": 0.46162403,
      "ingested_at": "2025-11-29T02:11:05.023299Z"
    },
    {
      "id": "tavily_d0627753",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Climate Change Ravages South-West Pacific: Rising Seas ...",
      "content": "The WMO report says that sea-level rise rates were, in general, slightly higher than the global mean rate, reaching approximately 4 mm per year",
      "url": "https://www.news18.com/world/climate-change-ravages-south-west-pacific-rising-seas-and-extreme-events-threaten-region-8540889.html",
      "published_at": "2025-11-29T02:11:05.023305Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:news18.com Are seawater levels rising around the world?",
      "relevance_score": 0.46075046,
      "ingested_at": "2025-11-29T02:11:05.023308Z"
    },
    {
      "id": "tavily_fe17d005",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "'Scary' Changes: NASA Highlights Human Influence On ...",
      "content": "This process is responsible for one-third to half of the rise in sea levels worldwide. According to scientists, the upper 700 metres of the",
      "url": "https://www.news18.com/viral/scary-changes-nasa-highlights-human-influence-on-ocean-temperatures-8944543.html",
      "published_at": "2025-11-29T02:11:05.023314Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:news18.com Are seawater levels rising around the world?",
      "relevance_score": 0.418341,
      "ingested_at": "2025-11-29T02:11:05.023318Z"
    },
    {
      "id": "tavily_dcdf9d11",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "In Sundarbans, rising sea levels have turned farms into ...",
      "content": "Scientists say seas around the world are rising due to climate change, but the Bay of Bengal is rising twice as fast as the global average.",
      "url": "https://scroll.in/article/865138/in-sundarbans-rising-sea-levels-have-turned-farms-into-wasteland-threatening-to-displace-millions",
      "published_at": "2025-11-29T02:11:05.697954Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:scroll.in Are seawater levels rising around the world?",
      "relevance_score": 0.64020914,
      "ingested_at": "2025-11-29T02:11:05.697973Z"
    },
    {
      "id": "tavily_f7ffc928",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "New NASA research points to an 'unavoidable' rise of ...",
      "content": "According to the US space agency, seas around the world have risen an average of three inches (7.6 cm) since 1992, and as much as nine inches (",
      "url": "https://scroll.in/article/751827/new-nasa-research-points-to-an-unavoidable-rise-of-several-feet-for-the-earths-oceans",
      "published_at": "2025-11-29T02:11:05.697983Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:scroll.in Are seawater levels rising around the world?",
      "relevance_score": 0.6211049,
      "ingested_at": "2025-11-29T02:11:05.697987Z"
    },
    {
      "id": "tavily_41e35cf6",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea level rise is real – which is why we need to retreat from ...",
      "content": "Coastal communities around the world are being increasingly exposed to the hazards of rising sea levels, with global sea levels found to be",
      "url": "https://scroll.in/article/773689/sea-level-rise-is-real-which-is-why-we-need-to-retreat-from-unrealistic-advice",
      "published_at": "2025-11-29T02:11:05.697994Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:scroll.in Are seawater levels rising around the world?",
      "relevance_score": 0.5803764,
      "ingested_at": "2025-11-29T02:11:05.697997Z"
    },
    {
      "id": "tavily_e0ab29cd",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "We may lose half the world's sandy beaches to sea-level ...",
      "content": "The rate at which sea levels are rising is accelerating by about 0.1mm per year each year. But sea level rise won't be even across the globe.",
      "url": "https://scroll.in/article/955056/high-alert-we-may-lose-half-the-worlds-sandy-beaches-to-sea-level-rise-by-2100",
      "published_at": "2025-11-29T02:11:05.698003Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:scroll.in Are seawater levels rising around the world?",
      "relevance_score": 0.53473455,
      "ingested_at": "2025-11-29T02:11:05.698006Z"
    },
    {
      "id": "tavily_39ef0da7",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Scientists looked at sea levels 125000 years ago. ...",
      "content": "Global average sea level is currently estimated to be rising at more than 3 millimetres a year. This rate is projected to increase and total",
      "url": "https://scroll.in/article/943078/scientists-looked-at-sea-levels-125000-years-ago-the-results-were-terrifying",
      "published_at": "2025-11-29T02:11:05.698011Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:scroll.in Are seawater levels rising around the world?",
      "relevance_score": 0.5126688,
      "ingested_at": "2025-11-29T02:11:05.698015Z"
    },
    {
      "id": "tavily_9f55a43e",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Satellite to track rising seas as climate warms",
      "content": "Satellites tracking the world's oceans since 1993 show that global mean sea level has risen, on average, by over three millimetres (more ...See more",
      "url": "https://www.deccanherald.com/science/satellite-to-track-rising-seas-as-climate-warms-918066.html",
      "published_at": "2025-11-29T02:11:06.363023Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
      "relevance_score": 0.528607,
      "ingested_at": "2025-11-29T02:11:06.363029Z"
    },
    {
      "id": "tavily_a359b114",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Sea level may be rising faster than thought: Study",
      "content": "The global sea level may be rising faster than previously thought, according to a study which suggests that the current measurement method",
      "url": "https://www.deccanherald.com/science/sea-level-may-be-rising-faster-715856.html",
      "published_at": "2025-11-29T02:11:06.363033Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
      "relevance_score": 0.5201313,
      "ingested_at": "2025-11-29T02:11:06.363034Z"
    },
    {
      "id": "tavily_fc4fa030",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Satellite snafu masked true sea-level rise",
      "content": "If sea level rise continues to accelerate at the current rate, Steven says, the world's oceans could rise by about 75 cm over the next century.See more",
      "url": "https://www.deccanherald.com/science/satellite-snafu-masked-true-sea-2016837",
      "published_at": "2025-11-29T02:11:06.363036Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
      "relevance_score": 0.5120832,
      "ingested_at": "2025-11-29T02:11:06.363037Z"
    },
    {
      "id": "tavily_cf3cecfc",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "A red signal: Oceans are turning green",
      "content": "Sea levels are already rising because of the melting of glaciers. This leads to fall in oxygen levels in the oceans and the death of fish on a ...See more",
      "url": "https://www.deccanherald.com/opinion/editorial/a-red-signal-oceans-are-turning-green-2652933",
      "published_at": "2025-11-29T02:11:06.363039Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
      "relevance_score": 0.48162505,
      "ingested_at": "2025-11-29T02:11:06.363040Z"
    },
    {
      "id": "tavily_2fba5d80",
      "source_type": "tavily",
      "source_name": "Tavily Search",
      "source_url": "https://api.tavily.com",
      "title": "Warming signs: An alarm for Asia",
      "content": "The UAE, Bahrain, Oman, and Iran suffered from excessive rains. Sea levels are rising, putting coastal communities at risk, and altering marine",
      "url": "https://www.deccanherald.com/opinion/editorial/warming-signs-an-alarm-for-asia-global-warming-emissions-climate-change-world-wide-3611454",
      "published_at": "2025-11-29T02:11:06.363042Z",
      "author": null,
      "categories": [
        
      ],
      "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
      "relevance_score": 0.45377067,
      "ingested_at": "2025-11-29T02:11:06.363044Z"
    }
  ],
  "classifications": {
    "cluster_0": {
      "is_misinformation": true,
      "confidence": 0.95,
      "classification": "misinformation",
      "topic_representation": "Claims about vaccine safety and side effects, as well as government health guidelines and water contamination rumors",
      "evidence_chain": [
        {
          "step": 1,
          "evidence": "Rapid growth of articles with no credible sources, indicating potential misinformation",
          "weight": 0.3,
          "indicator": "rapid_growth"
        },
        {
          "step": 2,
          "evidence": "Presence of contradictions and narrative evolution, suggesting a lack of factual accuracy",
          "weight": 0.4,
          "indicator": "contradictions"
        },
        {
          "step": 3,
          "evidence": "Low credibility of sources, with only a few credible sources present, indicating a high risk of misinformation",
          "weight": 0.3,
          "indicator": "low_credibility"
        }
      ],
      "key_indicators": [
        "Rapid growth",
        "Contradictions",
        "Low credibility"
      ],
      "reasoning": "Based on the analysis, this cluster exhibits multiple red flags for misinformation, including rapid growth, contradictions, and low credibility of sources. The presence of these indicators, combined with a high risk score, suggests a high likelihood of misinformation. The topic representation highlights the main subject of the cluster, which is claims about vaccine safety and side effects, as well as government health guidelines and water contamination rumors.",
      "supporting_evidence": [
        "The cluster has a high risk score of 0.746, indicating a high likelihood of misinformation.",
        "The presence of contradictions and narrative evolution suggests a lack of factual accuracy.",
        "The low credibility of sources, with only a few credible sources present, indicates a high risk of misinformation."
      ],
      "contradictory_evidence": [
        "The cluster does contain some credible sources, such as AP News and Reuters Health, which may indicate some legitimate news coverage.",
        "The topic representation is focused on claims about vaccine safety and side effects, which may be a legitimate area of discussion."
      ]
    }
  },
  "summary": {
    "total_clusters": 2,
    "total_classifications": 1,
    "ingestion_stats": {
      "total": 49,
      "processed": 0,
      "stored": 0,
      "skipped_duplicates": 49,
      "retrieved_duplicates": 49,
      "failed": 0,
      "errors": [
        
      ],
      "retrieved_duplicates_list": [
        {
          "id": "tavily_91feb6ef",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea levels are rising faster than in 4000 years",
          "content": "Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate change and melting ice. This poses a severe",
          "url": "https://timesofindia.indiatimes.com/etimes/trending/sea-levels-are-rising-faster-than-in-4000-years-hidden-threats-to-cities-causes-and-impacts/articleshow/124722208.cms",
          "published_at": "2025-11-29T01:02:31.327000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.327000Z",
          "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.6453216
        },
        {
          "id": "tavily_8490d888",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea level rise getting faster, finds new study",
          "content": "Environment News: Global sea levels are rising significantly faster than earlier thought, according to a new Harvard study.",
          "url": "https://timesofindia.indiatimes.com/home/environment/global-warming/Sea-level-rise-getting-faster-finds-new-study/articleshow/45899326.cms",
          "published_at": "2025-11-29T02:04:12.492000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:12.492000Z",
          "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.61168414
        },
        {
          "id": "tavily_11ea30de",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Nasa study shows interplay of El Niño and La Niña cycles ...",
          "content": "New data indicates that global sea levels are rising at an accelerating rate, posing an increased threat of flooding and coastal erosion. Recent",
          "url": "https://timesofindia.indiatimes.com/science/nasa-study-shows-interplay-of-el-nio-and-la-nia-cycles-impacts-global-sea-levels/articleshow/110935630.cms",
          "published_at": "2025-11-29T02:04:12.492000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:12.492000Z",
          "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.6108487
        },
        {
          "id": "tavily_50a68002",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Arabian Sea may rise by nearly 3ft over greenhouse effect",
          "content": "Global sea levels are rising because of human-caused global warming, with recent rates being unprecedented over the past 2,500-plus years.",
          "url": "https://timesofindia.indiatimes.com/city/pune/arabian-sea-may-rise-by-nearly-3ft-over-greenhouse-effect/articleshow/103562742.cms",
          "published_at": "2025-11-29T01:02:31.327000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.327000Z",
          "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.5993685
        },
        {
          "id": "tavily_bbf1b89b",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Global sea level surging at faster rate: Study",
          "content": "WASHINGTON: The global sea level is not rising at a steady rate, it is accelerating a little every year, according to a new assessment based on 25 years of",
          "url": "https://timesofindia.indiatimes.com/home/environment/global-warming/global-sea-level-surging-at-faster-rate-study/articleshow/62899291.cms",
          "published_at": "2025-11-29T01:02:31.327000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.327000Z",
          "search_query": "site:timesofindia.indiatimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.5914643
        },
        {
          "id": "tavily_c381b085",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Antarctica Sees Similar Climate Change Effects As ...",
          "content": "home     World News     Antarctica Sees Similar Climate Change Effects As Greenland: Study ## If Greenland's ice sheet were to melt entirely, global sea levels would rise by about seven metres (23 feet). If this were to occur in Antarctica, the sea level rise could exceed 50 metres. The planet's warming climate is having effects in Antarctica that increasingly resemble those observed in the Arctic, meaning global sea levels could rise faster that previously predicted, Danish researchers warned on Friday. If this were to occur in Antarctica, the sea level rise could exceed 50 metres, DMI said. Track Latest News Live on NDTV.com and get news updates from India  and around the world",
          "url": "https://www.ndtv.com/world-news/antarctica-sees-similar-climate-change-effects-as-greenland-study-9389880",
          "published_at": "2025-11-29T02:04:13.196000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:13.196000Z",
          "search_query": "site:ndtv.com Are seawater levels rising around the world?",
          "relevance_score": 0.6844544
        },
        {
          "id": "tavily_e1468092",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea Level Will Rise by 1 Meter, It's Unavoidable: NASA",
          "content": "Sea levels are rising around the world, and the latest satellite data suggests that three feet (one meter) or more is unavoidable in the",
          "url": "https://www.ndtv.com/world-news/nasa-sees-unavoidable-sea-level-rise-ahead-1211395",
          "published_at": "2025-11-29T01:02:31.975000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.975000Z",
          "search_query": "site:ndtv.com Are seawater levels rising around the world?",
          "relevance_score": 0.6824261
        },
        {
          "id": "tavily_3d81a31d",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Video: NASA Tracks 30 Years of Sea Level Rise In A New ...",
          "content": "Global average sea levels have risen faster since 1900. The Average sea level around the globe is increasing as the planet Earth warms and",
          "url": "https://www.ndtv.com/feature/video-nasa-tracks-30-years-of-sea-level-rise-in-a-new-terrifying-animation-4140432",
          "published_at": "2025-11-29T01:02:31.975000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.975000Z",
          "search_query": "site:ndtv.com Are seawater levels rising around the world?",
          "relevance_score": 0.54666615
        },
        {
          "id": "tavily_e1413efa",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Rise in Sea Level Doubled in Three Decades, Say ...",
          "content": "The rise of sea level in the world is around three millimetres per year, which is double the rate three decades ago, a senior scientist said",
          "url": "https://www.ndtv.com/goa-news/rise-in-sea-level-doubled-in-three-decades-say-researchers-575644",
          "published_at": "2025-11-29T01:02:31.975000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.975000Z",
          "search_query": "site:ndtv.com Are seawater levels rising around the world?",
          "relevance_score": 0.502564
        },
        {
          "id": "tavily_15de172b",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea Levels Rise",
          "content": "Over 100 Million Buildings Worldwide Could Face Flooding Risk From Rising Seas, Study Warns.",
          "url": "https://www.ndtv.com/topic/sea-levels-rise",
          "published_at": "2025-11-29T01:02:31.975000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:31.975000Z",
          "search_query": "site:ndtv.com Are seawater levels rising around the world?",
          "relevance_score": 0.45318982
        },
        {
          "id": "tavily_8a163ba7",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Explained | How rising sea levels threaten agriculture, ...",
          "content": "The world's sea level is rising at an unprecedented rate, portending potentially disastrous consequences for the weather, agriculture, the extant groundwater",
          "url": "https://www.thehindu.com/sci-tech/energy-and-environment/rising-sea-levels-threaten-agriculture-rainfall-social-fabric/article66781156.ece",
          "published_at": "2025-11-29T01:02:32.684000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:32.684000Z",
          "search_query": "site:thehindu.com Are seawater levels rising around the world?",
          "relevance_score": 0.4066976
        },
        {
          "id": "tavily_114b0ab4",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea levels around Indian coastlines projected to rise up ...",
          "content": "According to the latest IPCC Sixth Assessment Report, the global mean sea level has been rising over the last century at a rate of 1.8 mm/year.",
          "url": "https://www.thehindu.com/news/national/telangana/sea-levels-around-indian-coastlines-projected-to-rise-up-to-1-metre-by-2100-incois-study/article70303156.ece",
          "published_at": "2025-11-29T01:02:32.684000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:32.684000Z",
          "search_query": "site:thehindu.com Are seawater levels rising around the world?",
          "relevance_score": 0.56690645
        },
        {
          "id": "tavily_6c8e05a9",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea level rise cannot be pumped away - Frontline - The Hindu",
          "content": "Under unabated warming, sea level rise may exceed 130 cm by 2100. Climate scientists at the Potsdam Institute for Climate Impact (PIK), Germany,",
          "url": "https://frontline.thehindu.com/science-and-technology/sea-level-rise-cannot-be-pumped-away/article8466317.ece",
          "published_at": "2025-11-29T01:02:32.684000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:32.684000Z",
          "search_query": "site:thehindu.com Are seawater levels rising around the world?",
          "relevance_score": 0.48074743
        },
        {
          "id": "tavily_daa1c139",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "As oceans rise, are some nations doomed to vanish?",
          "content": "India   World   Movies   Sport   Data   Health   Opinion   Science   Business   Premium The prospect is no longer science fiction as global warming gathers pace, posing an unprecedented challenge to the international community, and threatening entire peoples with the loss of their land and identity. This is still below the highest point of the smallest, flattest island states, but rising seas will be accompanied by an increase in storms and tidal surges: Salt contamination to water and land will make many atolls uninhabitable long before they are covered over by the sea. In an August 2021 declaration, the members of the Pacific Islands Forum, including Australia and New Zealand, proclaimed that their maritime zones \"shall continue to apply, without reduction, notwithstanding any physical changes connected to climate change-related sea level rise.\"",
          "url": "https://www.thehindu.com/sci-tech/energy-and-environment/as-oceans-rise-are-some-nations-doomed-to-vanish/article65991818.ece",
          "published_at": "2025-11-29T02:04:13.883000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:13.883000Z",
          "search_query": "site:thehindu.com Are seawater levels rising around the world?",
          "relevance_score": 0.39459804
        },
        {
          "id": "tavily_657dc7ef",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Data show seas rising faster around Maldives ...",
          "content": "September 1, 2025e-Paper Account Opinion   Editorial   Cartoon   Columns   Comment   Interview   Lead   Letters   Open Page   Corrections & Clarifications Education Education   Careers   Colleges   Schools September 1, 2025e-Paper Published - September 01, 2025 05:15 am IST Published - September 01, 2025 05:15 am IST * Access to comment on every story ### Comments Comments have to be in English, and in full sentences. Please abide by our community guidelines  for posting your comments. We have migrated to a new commenting platform. If you are already a registered user of The Hindu and logged in, you may continue to engage with our articles. If you do not have an account please register and login to post comments. Users can access their older comments by logging into their accounts on Vuukle.",
          "url": "https://www.thehindu.com/sci-tech/science/data-show-seas-rising-faster-around-maldives-lakshadweep-than-believed/article69996142.ece",
          "published_at": "2025-11-29T02:04:13.883000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:13.883000Z",
          "search_query": "site:thehindu.com Are seawater levels rising around the world?",
          "relevance_score": 0.38706517
        },
        {
          "id": "tavily_a9589aea",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Almost 2 cm of sea level rise this century was due to ...",
          "content": "Simply put, global sea levels have risen by more than 10 cm between 1993 and 2024, according to NASA, which says that the recent rate of",
          "url": "https://indianexpress.com/article/explained/explained-climate/melting-glaciers-2-cm-sea-level-rise-9849231/",
          "published_at": "2025-11-29T01:02:33.339000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.339000Z",
          "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
          "relevance_score": 0.46104163
        },
        {
          "id": "tavily_940c6c2e",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "36 million Indians may face annual floods by 2050 due to ...",
          "content": "It had showed that while sea level rose globally around 15 cm during the 20th century, it is currently rising at more than twice the speed — 3. ...See more",
          "url": "https://indianexpress.com/article/india/36-million-indians-may-face-annual-floods-by-2050-due-to-sea-level-rise-study-6093630/",
          "published_at": "2025-11-29T02:04:14.542000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:14.542000Z",
          "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
          "relevance_score": 0.5510187
        },
        {
          "id": "tavily_aa380693",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Mumbai, Dhaka, London, New York among metros in line ...",
          "content": "India, China, Bangladesh and the Netherlands face the highest threat of sea-level rise globally, according to a new report by the World Meteorological",
          "url": "https://indianexpress.com/article/india/mumbai-dhaka-london-new-york-among-metros-in-line-of-sea-level-rise-threat-report-8445371/",
          "published_at": "2025-11-29T01:02:33.339000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.339000Z",
          "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
          "relevance_score": 0.528753
        },
        {
          "id": "tavily_047e7430",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "World's mangroves, marshes & coral could be devastated ...",
          "content": "A similar rise in sea levels could happen due to human-caused global warming today, devastating coastal agriculture around the world.",
          "url": "https://indianexpress.com/article/technology/science/world-mangrove-marshes-coral-sea-level-rise-8925444/",
          "published_at": "2025-11-29T01:02:33.339000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.339000Z",
          "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
          "relevance_score": 0.5065188
        },
        {
          "id": "tavily_d0a61639",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Digging Deep: Deltas losing land due to rising sea levels ...",
          "content": "Rising sea levels and human intervention in rivers are rapidly changing river-dynamics across the world. Read more below in today's edition",
          "url": "https://indianexpress.com/article/technology/science/digging-deep-deltas-losing-land-due-to-rising-sea-levels-and-rivers-changing-course-8086106/",
          "published_at": "2025-11-29T02:04:14.542000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:14.542000Z",
          "search_query": "site:indianexpress.com Are seawater levels rising around the world?",
          "relevance_score": 0.47957736
        },
        {
          "id": "tavily_2e120501",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea-levels could rise up to 4 ft by end of century due ...",
          "content": "Sea-levels could rise up to 4 ft by end of century due to global warming, warn scientists | Hindustan Times.",
          "url": "https://www.hindustantimes.com/science/sea-levels-could-rise-up-to-4-ft-by-end-of-century-due-to-global-warming-warn-scientists/story-LtFEGbRBkXnAXExYeaKINN.html",
          "published_at": "2025-11-29T01:02:33.995000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.995000Z",
          "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.6862234
        },
        {
          "id": "tavily_c0bca29c",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Global warming is destroying Costa Rica's coastline, ...",
          "content": "Global warming could cause sea levels around the world to rise between 70 cm and 1.2 metres (28-47 inches) in the next two centuries, ramping",
          "url": "https://www.hindustantimes.com/travel/how-global-warming-is-destroying-costa-rica-s-coastline-threatening-tourism/story-3AA3tgLpRpRqFkMEMfmcSP.html",
          "published_at": "2025-11-29T01:02:33.995000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.995000Z",
          "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.5911811
        },
        {
          "id": "tavily_08cd133f",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "NASA visualises how sea levels will rise in Indian coastal ...",
          "content": "Global mean sea level increased by 0.20m between 1901 and 2018. Sea level around Asia in the North Indian Ocean has increased faster than",
          "url": "https://www.hindustantimes.com/environment/nasa-visualises-how-sea-levels-will-rise-in-indian-coastal-regions-101629257135231.html",
          "published_at": "2025-11-29T01:02:33.995000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.995000Z",
          "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.5462305
        },
        {
          "id": "tavily_cbcc5029",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea-level rise a major threat to India, other nations: WMO",
          "content": "Global mean sea-level increased by 0.20m between 1901 and 2018, with an average rate increase of 1.3 mm/ year between 1901 and 1971,1.9",
          "url": "https://www.hindustantimes.com/india-news/sealevel-rise-a-major-threat-to-india-other-nations-wmo-101676400422024.html",
          "published_at": "2025-11-29T01:02:33.995000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:33.995000Z",
          "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.5150107
        },
        {
          "id": "tavily_317242e2",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "It's time for Northeast to prep for floods like those that hit ...",
          "content": "Worldwide, sea levels have risen faster since 1900, putting hundreds of millions of people at risk, the United Nations has said.",
          "url": "https://www.hindustantimes.com/world-news/its-time-for-northeast-to-prep-for-floods-like-those-that-hit-this-winter-climate-change-is-why-101707973890571.html",
          "published_at": "2025-11-29T02:04:15.200000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:15.200000Z",
          "search_query": "site:hindustantimes.com Are seawater levels rising around the world?",
          "relevance_score": 0.5150107
        },
        {
          "id": "tavily_b30ced11",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Global sea level surging at faster rate, says study - Mint",
          "content": "Washington: The global sea level is not rising at a steady rate, it is accelerating a little every year, according to a new assessment based",
          "url": "https://www.livemint.com/Science/OP5KylsYDrsFtx64xlHEqK/Global-sea-level-surging-at-faster-rate-says-study.html",
          "published_at": "2025-11-29T01:02:34.665000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:34.665000Z",
          "search_query": "site:livemint.com Are seawater levels rising around the world?",
          "relevance_score": 0.7092009
        },
        {
          "id": "tavily_83a9a54b",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea levels rising faster than predicted: Nasa scientists - Mint",
          "content": "The world's oceans have risen an average of almost 3 inches since 1992, due to global warming, say Nasa researchers.",
          "url": "https://www.livemint.com/Politics/VHt3v3xOaL9Wytkp5WkbvO/Warming-seas-rising-faster-than-predicted-Nasa.html",
          "published_at": "2025-11-29T01:02:34.665000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:34.665000Z",
          "search_query": "site:livemint.com Are seawater levels rising around the world?",
          "relevance_score": 0.70750624
        },
        {
          "id": "tavily_ca02a456",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "In Hot Water - Mint",
          "content": "And if atmospheric temperatures are rising around the world, it is because the ocean is nearly saturated with an unnatural amount of heat.",
          "url": "https://livemint.com/mint-top-newsletter/climate-change12122024.html",
          "published_at": "2025-11-29T01:02:34.665000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:34.665000Z",
          "search_query": "site:livemint.com Are seawater levels rising around the world?",
          "relevance_score": 0.6426349
        },
        {
          "id": "tavily_cc5d7c6a",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Rising sea levels may sink Mumbai by 2100: IPCC report - Mint",
          "content": "Global sea levels are set to rise by at least 1m by 2100 if carbon emissions go unchecked, submerging hundreds of cities, including Mumbai and Kolkata.",
          "url": "https://www.livemint.com/news/india/rising-sea-levels-may-sink-mumbai-by-2100-ipcc-report-1569436019802.html",
          "published_at": "2025-11-29T01:02:34.665000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:34.665000Z",
          "search_query": "site:livemint.com Are seawater levels rising around the world?",
          "relevance_score": 0.6391287
        },
        {
          "id": "tavily_f7bbca16",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Ocean warming has almost doubled in the last decade: Study",
          "content": "“The world ocean, in 2023, is now the hottest ever recorded, and sea levels are rising because heat causes water to expand and ice to melt,”",
          "url": "https://www.livemint.com/mint-lounge/business-of-life/ocean-warming-doubled-greenhouse-gas-111699013336640.html",
          "published_at": "2025-11-29T02:04:15.864000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:15.864000Z",
          "search_query": "site:livemint.com Are seawater levels rising around the world?",
          "relevance_score": 0.62879556
        },
        {
          "id": "tavily_570ca3c2",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Global sea levels may rise by 2300 if greenhouse gas ...",
          "content": "From 2000 to 2050, global average sea-level will most likely rise about 6 to 10 inches, but is extremely unlikely to rise by more than 18 inches",
          "url": "https://www.business-standard.com/article/current-affairs/global-sea-levels-may-rise-by-2300-if-greenhouse-gas-emissions-remain-high-118100800453_1.html",
          "published_at": "2025-11-29T01:02:35.328000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:35.328000Z",
          "search_query": "site:business-standard.com Are seawater levels rising around the world?",
          "relevance_score": 0.53094244
        },
        {
          "id": "tavily_504e5ee4",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Rising seas 'worldwide catastrophe' affecting Pacific ...",
          "content": "Globally, sea level rise has been accelerating, the UN report said, echoing peer-reviewed studies. The rate is now the fastest it has been in 3",
          "url": "https://www.business-standard.com/world-news/rising-seas-worldwide-catastrophe-affecting-pacific-paradises-un-chief-124082700056_1.html",
          "published_at": "2025-11-29T01:02:35.328000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:35.328000Z",
          "search_query": "site:business-standard.com Are seawater levels rising around the world?",
          "relevance_score": 0.45289946
        },
        {
          "id": "tavily_6f96b56a",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Global sea levels could rise 2m by the end of century, finds ...",
          "content": "Global sea levels could rise by two metres (6.5 feet) and displace tens of millions of people by the end of the century, according to new",
          "url": "https://www.business-standard.com/article/pti-stories/2-metre-sea-level-rise-plausible-by-2100-study-119052101264_1.html",
          "published_at": "2025-11-29T01:02:35.328000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:35.328000Z",
          "search_query": "site:business-standard.com Are seawater levels rising around the world?",
          "relevance_score": 0.4292146
        },
        {
          "id": "tavily_f7ab5260",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea levels to rise 10-12 inches by 2050, rate alarming",
          "content": "Sea levels along US coastlines will rise between 10 to 12 inches (25 to 30 cm) on average above the current levels by 2050, according to a",
          "url": "https://www.business-standard.com/article/international/sea-levels-to-rise-10-12-inches-by-2050-rate-alarming-report-122021700192_1.html",
          "published_at": "2025-11-29T01:02:35.328000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:35.328000Z",
          "search_query": "site:business-standard.com Are seawater levels rising around the world?",
          "relevance_score": 0.41648865
        },
        {
          "id": "tavily_945e5a17",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Glaciers Are Melting But Antarctica's Sea Levels ...",
          "content": "# Glaciers Are Melting But Antarctica’s Sea Levels Are Falling Instead Of Rising. Antarctica's ice melt lowers local sea levels due to reduced gravity but raises global levels. This dramatic reversal is considered one of the most remarkable natural processes, and a new study has revealed a surprising twist: as Antarctica’s ice melts, global sea levels will rise, yet the sea level around Antarctica itself will actually fall. As a result, sea levels fall close to Antarctica, while rising rapidly across the rest of the world. 1. **Isostatic rebound:** As ice mass reduces, the land beneath Antarctica slowly rises, lifting some ice away from warm ocean waters and slowing melting. News world  Glaciers Are Melting But Antarctica’s Sea Levels Are Falling Instead Of Rising.",
          "url": "https://www.news18.com/world/glaciers-are-melting-but-antarcticas-sea-levels-are-falling-instead-of-rising-heres-why-ws-akl-9737211.html",
          "published_at": "2025-11-29T01:02:35.988000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:35.988000Z",
          "search_query": "site:news18.com Are seawater levels rising around the world?",
          "relevance_score": 0.6407488
        },
        {
          "id": "tavily_0caedd81",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "World Oceans Day 2022: Do You Know These Cool Facts ...",
          "content": "Rising sea levels, more frequent powerful storms, plastic pollution and much more has threatened the health of oceans.",
          "url": "https://www.news18.com/news/lifestyle/world-oceans-day-2022-do-you-know-these-cool-facts-about-oceans-5326231.html",
          "published_at": "2025-11-29T02:04:17.218000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:17.218000Z",
          "search_query": "site:news18.com Are seawater levels rising around the world?",
          "relevance_score": 0.4654124
        },
        {
          "id": "tavily_93f8b86b",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Melting Atlantic Glacier Will Increase Sea-level by 20 ...",
          "content": "Global warming is causing our glaciers to melt faster and our sea level is rising by an alarming global average of 3.3 millimetres per year",
          "url": "https://www.news18.com/news/buzz/melting-atlantic-glacier-will-increase-sea-level-by-20-percent-more-than-previously-predicted-3706526.html",
          "published_at": "2025-11-29T01:02:35.988000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:35.988000Z",
          "search_query": "site:news18.com Are seawater levels rising around the world?",
          "relevance_score": 0.4617697
        },
        {
          "id": "tavily_d0627753",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Climate Change Ravages South-West Pacific: Rising Seas ...",
          "content": "The WMO report says that sea-level rise rates were, in general, slightly higher than the global mean rate, reaching approximately 4 mm per year",
          "url": "https://www.news18.com/world/climate-change-ravages-south-west-pacific-rising-seas-and-extreme-events-threaten-region-8540889.html",
          "published_at": "2025-11-29T02:04:17.218000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:17.218000Z",
          "search_query": "site:news18.com Are seawater levels rising around the world?",
          "relevance_score": 0.46075046
        },
        {
          "id": "tavily_fe17d005",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "'Scary' Changes: NASA Highlights Human Influence On ...",
          "content": "This process is responsible for one-third to half of the rise in sea levels worldwide. According to scientists, the upper 700 metres of the",
          "url": "https://www.news18.com/viral/scary-changes-nasa-highlights-human-influence-on-ocean-temperatures-8944543.html",
          "published_at": "2025-11-29T02:04:17.218000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:17.218000Z",
          "search_query": "site:news18.com Are seawater levels rising around the world?",
          "relevance_score": 0.418341
        },
        {
          "id": "tavily_dcdf9d11",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "In Sundarbans, rising sea levels have turned farms into ...",
          "content": "Scientists say seas around the world are rising due to climate change, but the Bay of Bengal is rising twice as fast as the global average.",
          "url": "https://scroll.in/article/865138/in-sundarbans-rising-sea-levels-have-turned-farms-into-wasteland-threatening-to-displace-millions",
          "published_at": "2025-11-29T01:02:36.676000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:36.676000Z",
          "search_query": "site:scroll.in Are seawater levels rising around the world?",
          "relevance_score": 0.64020914
        },
        {
          "id": "tavily_f7ffc928",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "New NASA research points to an 'unavoidable' rise of ...",
          "content": "According to the US space agency, seas around the world have risen an average of three inches (7.6 cm) since 1992, and as much as nine inches (",
          "url": "https://scroll.in/article/751827/new-nasa-research-points-to-an-unavoidable-rise-of-several-feet-for-the-earths-oceans",
          "published_at": "2025-11-29T01:02:36.676000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:36.676000Z",
          "search_query": "site:scroll.in Are seawater levels rising around the world?",
          "relevance_score": 0.6211049
        },
        {
          "id": "tavily_41e35cf6",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea level rise is real – which is why we need to retreat from ...",
          "content": "Coastal communities around the world are being increasingly exposed to the hazards of rising sea levels, with global sea levels found to be",
          "url": "https://scroll.in/article/773689/sea-level-rise-is-real-which-is-why-we-need-to-retreat-from-unrealistic-advice",
          "published_at": "2025-11-29T01:02:36.676000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:36.676000Z",
          "search_query": "site:scroll.in Are seawater levels rising around the world?",
          "relevance_score": 0.5803764
        },
        {
          "id": "tavily_e0ab29cd",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "We may lose half the world's sandy beaches to sea-level ...",
          "content": "The rate at which sea levels are rising is accelerating by about 0.1mm per year each year. But sea level rise won't be even across the globe.",
          "url": "https://scroll.in/article/955056/high-alert-we-may-lose-half-the-worlds-sandy-beaches-to-sea-level-rise-by-2100",
          "published_at": "2025-11-29T01:02:36.676000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:36.676000Z",
          "search_query": "site:scroll.in Are seawater levels rising around the world?",
          "relevance_score": 0.53473455
        },
        {
          "id": "tavily_39ef0da7",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Scientists looked at sea levels 125000 years ago. ...",
          "content": "Global average sea level is currently estimated to be rising at more than 3 millimetres a year. This rate is projected to increase and total",
          "url": "https://scroll.in/article/943078/scientists-looked-at-sea-levels-125000-years-ago-the-results-were-terrifying",
          "published_at": "2025-11-29T01:02:36.676000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:36.676000Z",
          "search_query": "site:scroll.in Are seawater levels rising around the world?",
          "relevance_score": 0.5126688
        },
        {
          "id": "tavily_9f55a43e",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Satellite to track rising seas as climate warms",
          "content": "Satellites tracking the world's oceans since 1993 show that global mean sea level has risen, on average, by over three millimetres (more ...See more",
          "url": "https://www.deccanherald.com/science/satellite-to-track-rising-seas-as-climate-warms-918066.html",
          "published_at": "2025-11-29T02:04:18.543000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:18.544000Z",
          "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
          "relevance_score": 0.528607
        },
        {
          "id": "tavily_a359b114",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Sea level may be rising faster than thought: Study",
          "content": "The global sea level may be rising faster than previously thought, according to a study which suggests that the current measurement method",
          "url": "https://www.deccanherald.com/science/sea-level-may-be-rising-faster-715856.html",
          "published_at": "2025-11-29T01:02:37.336000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:37.336000Z",
          "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
          "relevance_score": 0.5201313
        },
        {
          "id": "tavily_fc4fa030",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Satellite snafu masked true sea-level rise",
          "content": "If sea level rise continues to accelerate at the current rate, Steven says, the world's oceans could rise by about 75 cm over the next century.See more",
          "url": "https://www.deccanherald.com/science/satellite-snafu-masked-true-sea-2016837",
          "published_at": "2025-11-29T02:04:18.544000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T02:04:18.544000Z",
          "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
          "relevance_score": 0.5120832
        },
        {
          "id": "tavily_cf3cecfc",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "A red signal: Oceans are turning green",
          "content": "Sea levels are already rising because of the melting of glaciers. This leads to fall in oxygen levels in the oceans and the death of fish on a",
          "url": "https://www.deccanherald.com/opinion/editorial/a-red-signal-oceans-are-turning-green-2652933",
          "published_at": "2025-11-29T01:02:37.336000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:37.336000Z",
          "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
          "relevance_score": 0.49538648
        },
        {
          "id": "tavily_2fba5d80",
          "source_type": "tavily",
          "source_name": "Tavily Search",
          "source_url": "https://api.tavily.com",
          "title": "Warming signs: An alarm for Asia",
          "content": "The UAE, Bahrain, Oman, and Iran suffered from excessive rains. Sea levels are rising, putting coastal communities at risk, and altering marine",
          "url": "https://www.deccanherald.com/opinion/editorial/warming-signs-an-alarm-for-asia-global-warming-emissions-climate-change-world-wide-3611454",
          "published_at": "2025-11-29T01:02:37.336000Z",
          "author": null,
          "categories": [
            
          ],
          "ingested_at": "2025-11-29T01:02:37.336000Z",
          "search_query": "site:deccanherald.com Are seawater levels rising around the world?",
          "relevance_score": 0.45377067
        }
      ]
    },
    "clustering_stats": {
      "clusters_found": 4,
      "total_datapoints": 154,
      "statistics": {
        "total_clusters": 4,
        "total_datapoints": 154,
        "avg_cluster_size": 38.5,
        "largest_cluster": 112,
        "smallest_cluster": 2,
        "cluster_size_distribution": {
          "small": 2,
          "medium": 0,
          "large": 2
        }
      }
    }
  },
  "clusters": {
    "cluster_0": {
      "topic_representation": "Sea levels are - Global Rising Levels Faster Level",
      "datapoints": [
        {
          "id": "tavily_91feb6ef",
          "title": "Sea levels are rising faster than in 4000 years",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_8490d888",
          "title": "Sea level rise getting faster, finds new study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:12.492000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_11ea30de",
          "title": "Nasa study shows interplay of El Niño and La Niña cycles ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:12.492000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_50a68002",
          "title": "Arabian Sea may rise by nearly 3ft over greenhouse effect",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_bbf1b89b",
          "title": "Global sea level surging at faster rate: Study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_c381b085",
          "title": "Antarctica Sees Similar Climate Change Effects As ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:13.196000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e1468092",
          "title": "Sea Level Will Rise by 1 Meter, It's Unavoidable: NASA",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_3d81a31d",
          "title": "Video: NASA Tracks 30 Years of Sea Level Rise In A New ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e1413efa",
          "title": "Rise in Sea Level Doubled in Three Decades, Say ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_15de172b",
          "title": "Sea Levels Rise",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_8a163ba7",
          "title": "Explained | How rising sea levels threaten agriculture, ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_114b0ab4",
          "title": "Sea levels around Indian coastlines projected to rise up ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_6c8e05a9",
          "title": "Sea level rise cannot be pumped away - Frontline - The Hindu",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_daa1c139",
          "title": "As oceans rise, are some nations doomed to vanish?",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:13.883000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_a9589aea",
          "title": "Almost 2 cm of sea level rise this century was due to ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_940c6c2e",
          "title": "36 million Indians may face annual floods by 2050 due to ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:14.542000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_aa380693",
          "title": "Mumbai, Dhaka, London, New York among metros in line ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_047e7430",
          "title": "World's mangroves, marshes & coral could be devastated ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_d0a61639",
          "title": "Digging Deep: Deltas losing land due to rising sea levels ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:14.542000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_2e120501",
          "title": "Sea-levels could rise up to 4 ft by end of century due ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_c0bca29c",
          "title": "Global warming is destroying Costa Rica's coastline, ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_08cd133f",
          "title": "NASA visualises how sea levels will rise in Indian coastal ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cbcc5029",
          "title": "Sea-level rise a major threat to India, other nations: WMO",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_317242e2",
          "title": "It's time for Northeast to prep for floods like those that hit ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:15.200000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_b30ced11",
          "title": "Global sea level surging at faster rate, says study - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_83a9a54b",
          "title": "Sea levels rising faster than predicted: Nasa scientists - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_ca02a456",
          "title": "In Hot Water - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cc5d7c6a",
          "title": "Rising sea levels may sink Mumbai by 2100: IPCC report - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_f7bbca16",
          "title": "Ocean warming has almost doubled in the last decade: Study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:15.864000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_570ca3c2",
          "title": "Global sea levels may rise by 2300 if greenhouse gas ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_504e5ee4",
          "title": "Rising seas 'worldwide catastrophe' affecting Pacific ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_6f96b56a",
          "title": "Global sea levels could rise 2m by the end of century, finds ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_f7ab5260",
          "title": "Sea levels to rise 10-12 inches by 2050, rate alarming",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_945e5a17",
          "title": "Glaciers Are Melting But Antarctica's Sea Levels ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_0caedd81",
          "title": "World Oceans Day 2022: Do You Know These Cool Facts ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:17.218000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_93f8b86b",
          "title": "Melting Atlantic Glacier Will Increase Sea-level by 20 ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_d0627753",
          "title": "Climate Change Ravages South-West Pacific: Rising Seas ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:17.218000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_fe17d005",
          "title": "'Scary' Changes: NASA Highlights Human Influence On ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:17.218000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_dcdf9d11",
          "title": "In Sundarbans, rising sea levels have turned farms into ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_f7ffc928",
          "title": "New NASA research points to an 'unavoidable' rise of ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_41e35cf6",
          "title": "Sea level rise is real – which is why we need to retreat from ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e0ab29cd",
          "title": "We may lose half the world's sandy beaches to sea-level ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_39ef0da7",
          "title": "Scientists looked at sea levels 125000 years ago. ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_9f55a43e",
          "title": "Satellite to track rising seas as climate warms",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:18.543000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_a359b114",
          "title": "Sea level may be rising faster than thought: Study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_fc4fa030",
          "title": "Satellite snafu masked true sea-level rise",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:18.544000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cf3cecfc",
          "title": "A red signal: Oceans are turning green",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_2fba5d80",
          "title": "Warming signs: An alarm for Asia",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_91feb6ef",
          "title": "Sea levels are rising faster than in 4000 years",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_8490d888",
          "title": "Sea level rise getting faster, finds new study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:12.492000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_11ea30de",
          "title": "Nasa study shows interplay of El Niño and La Niña cycles ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:12.492000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_50a68002",
          "title": "Arabian Sea may rise by nearly 3ft over greenhouse effect",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_bbf1b89b",
          "title": "Global sea level surging at faster rate: Study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_c381b085",
          "title": "Antarctica Sees Similar Climate Change Effects As ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:13.196000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e1468092",
          "title": "Sea Level Will Rise by 1 Meter, It's Unavoidable: NASA",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_3d81a31d",
          "title": "Video: NASA Tracks 30 Years of Sea Level Rise In A New ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e1413efa",
          "title": "Rise in Sea Level Doubled in Three Decades, Say ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_15de172b",
          "title": "Sea Levels Rise",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_8a163ba7",
          "title": "Explained | How rising sea levels threaten agriculture, ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_114b0ab4",
          "title": "Sea levels around Indian coastlines projected to rise up ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_6c8e05a9",
          "title": "Sea level rise cannot be pumped away - Frontline - The Hindu",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_daa1c139",
          "title": "As oceans rise, are some nations doomed to vanish?",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:13.883000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_a9589aea",
          "title": "Almost 2 cm of sea level rise this century was due to ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_940c6c2e",
          "title": "36 million Indians may face annual floods by 2050 due to ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:14.542000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_aa380693",
          "title": "Mumbai, Dhaka, London, New York among metros in line ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_047e7430",
          "title": "World's mangroves, marshes & coral could be devastated ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_d0a61639",
          "title": "Digging Deep: Deltas losing land due to rising sea levels ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:14.542000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_2e120501",
          "title": "Sea-levels could rise up to 4 ft by end of century due ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_c0bca29c",
          "title": "Global warming is destroying Costa Rica's coastline, ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_08cd133f",
          "title": "NASA visualises how sea levels will rise in Indian coastal ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cbcc5029",
          "title": "Sea-level rise a major threat to India, other nations: WMO",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_317242e2",
          "title": "It's time for Northeast to prep for floods like those that hit ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:15.200000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_b30ced11",
          "title": "Global sea level surging at faster rate, says study - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_83a9a54b",
          "title": "Sea levels rising faster than predicted: Nasa scientists - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_ca02a456",
          "title": "In Hot Water - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cc5d7c6a",
          "title": "Rising sea levels may sink Mumbai by 2100: IPCC report - Mint",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:34.665000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_f7bbca16",
          "title": "Ocean warming has almost doubled in the last decade: Study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:15.864000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_570ca3c2",
          "title": "Global sea levels may rise by 2300 if greenhouse gas ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_504e5ee4",
          "title": "Rising seas 'worldwide catastrophe' affecting Pacific ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_6f96b56a",
          "title": "Global sea levels could rise 2m by the end of century, finds ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_f7ab5260",
          "title": "Sea levels to rise 10-12 inches by 2050, rate alarming",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_945e5a17",
          "title": "Glaciers Are Melting But Antarctica's Sea Levels ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_0caedd81",
          "title": "World Oceans Day 2022: Do You Know These Cool Facts ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:17.218000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_93f8b86b",
          "title": "Melting Atlantic Glacier Will Increase Sea-level by 20 ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_d0627753",
          "title": "Climate Change Ravages South-West Pacific: Rising Seas ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:17.218000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_fe17d005",
          "title": "'Scary' Changes: NASA Highlights Human Influence On ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:17.218000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_dcdf9d11",
          "title": "In Sundarbans, rising sea levels have turned farms into ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_f7ffc928",
          "title": "New NASA research points to an 'unavoidable' rise of ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_41e35cf6",
          "title": "Sea level rise is real – which is why we need to retreat from ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e0ab29cd",
          "title": "We may lose half the world's sandy beaches to sea-level ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_39ef0da7",
          "title": "Scientists looked at sea levels 125000 years ago. ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:36.676000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_9f55a43e",
          "title": "Satellite to track rising seas as climate warms",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:18.543000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_a359b114",
          "title": "Sea level may be rising faster than thought: Study",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_fc4fa030",
          "title": "Satellite snafu masked true sea-level rise",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:18.544000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cf3cecfc",
          "title": "A red signal: Oceans are turning green",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_2fba5d80",
          "title": "Warming signs: An alarm for Asia",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_b758c5e3",
          "title": "'Historical records may underestimate global sea level rise'",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_dc971f4a",
          "title": "sea levels",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:37.336000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_eb88ad3c",
          "title": "Rise in Global Sea Levels Doubles with World Getting ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_1e0c1a24",
          "title": "Are Cyclones Getting Stronger? A Global Shift And India's ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_cf37db8c",
          "title": "Sea levels rising around the world, unavoidable: NASA",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.988000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_af60b375",
          "title": "Global sea level rose by 4.5 mm per year during 2013-22 ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:35.328000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_80dc8689",
          "title": "'Global sea levels rose by a factor of two within 10 years' ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.995000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_aee2205c",
          "title": "Warming up to climate change: Why does sea level rise ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_1967fded",
          "title": "Why are sea levels rising?",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:33.339000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_6b863454",
          "title": "Sea levels rising faster in Pacific than elsewhere, says ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_e3710436",
          "title": "Sea levels not rising: Swedish scientist",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:32.684000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_36807746",
          "title": "Sea Levels Rising Faster In Pacific Than Elsewhere: Report",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.975000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_3d26b3c1",
          "title": "Not just Venice is sinking! Here's the list of world's most ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_624da5dd",
          "title": "Sea levels rising faster, Indian cities at high flood risk: IPCC",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 01:02:31.327000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_8_4",
          "title": "Mumbai climate risk: Greater awareness has reflected in ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 00:40:35.004000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_6_1",
          "title": "Climate Change@ 2050: Why Mumbai may get that ' ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 00:40:25.487000",
          "categories": [
            
          ]
        }
      ],
      "relevance_score": 0.8126961982424881
    },
    "cluster_1": {
      "topic_representation": "Data show seas - Data Show Seas Rising Faster",
      "datapoints": [
        {
          "id": "tavily_657dc7ef",
          "title": "Data show seas rising faster around Maldives ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:13.883000",
          "categories": [
            
          ]
        },
        {
          "id": "tavily_657dc7ef",
          "title": "Data show seas rising faster around Maldives ...",
          "source_name": "Tavily Search",
          "source_type": "tavily",
          "published_at": "2025-11-29 02:04:13.883000",
          "categories": [
            
          ]
        }
      ],
      "relevance_score": 0.7292325414323261
    }
  },
  "pattern_analyses": {
    "cluster_0": {
      "cluster_id": "cluster_0",
      "datapoint_count": 81,
      "overall_risk_score": 0.746,
      "risk_level": "high",
      "flags": {
        "rapid_growth": true,
        "low_credibility": true,
        "has_contradictions": true,
        "narrative_evolution": true
      },
      "flag_count": 4,
      "growth_analysis": {
        "is_rapid_growth": true,
        "growth_rate": null,
        "current_size": 65,
        "previous_size": 0,
        "time_window_hours": 6,
        "datapoints_per_hour": 0.01,
        "total_datapoints": 81,
        "risk_score": 0.7,
        "first_datapoint_time": "2025-01-15T06:30:00",
        "last_datapoint_time": "2025-11-29T02:04:18.544000"
      },
      "credibility_analysis": {
        "credible_sources": [
          "AP News",
          "BBC News",
          "Reuters Health"
        ],
        "questionable_sources": [
          
        ],
        "credible_ratio": 0.099,
        "credible_count": 8,
        "questionable_count": 0,
        "source_diversity": 4,
        "total_sources": 81,
        "risk_score": 0.571,
        "source_breakdown": {
          "Reuters Health": 3,
          "Tavily Search": 73,
          "AP News": 4,
          "BBC News": 1
        },
        "fact_checkers_present": false,
        "meets_credibility_threshold": false
      },
      "contradiction_analysis": {
        "has_contradictions": true,
        "contradiction_count": 164,
        "contradiction_pairs": [
          {
            "claim1": {
              "id": "misinfo_003",
              "title": "Fact-checkers debunk viral claim about government health measures",
              "source": "AP News",
              "text": "Fact-checkers debunk viral claim about government health measures. Multiple fact-checking organizations have verified that a viral claim circulating o"
            },
            "claim2": {
              "id": "misinfo_004",
              "title": "False rumors about food safety spread online, officials clarify",
              "source": "Tavily Search",
              "text": "False rumors about food safety spread online, officials clarify. Health officials have clarified that rumors circulating online about food safety issu"
            },
            "similarity": 0.725,
            "contradiction_type": "fact_check_vs_claim"
          },
          {
            "claim1": {
              "id": "tavily_91feb6ef",
              "title": "Sea levels are rising faster than in 4000 years",
              "source": "Tavily Search",
              "text": "Sea levels are rising faster than in 4000 years. Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate cha"
            },
            "claim2": {
              "id": "tavily_bbf1b89b",
              "title": "Global sea level surging at faster rate: Study",
              "source": "Tavily Search",
              "text": "Global sea level surging at faster rate: Study. WASHINGTON: The global sea level is not rising at a steady rate, it is accelerating a little every yea"
            },
            "similarity": 0.798,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_91feb6ef",
              "title": "Sea levels are rising faster than in 4000 years",
              "source": "Tavily Search",
              "text": "Sea levels are rising faster than in 4000 years. Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate cha"
            },
            "claim2": {
              "id": "tavily_3d26b3c1",
              "title": "Not just Venice is sinking! Here's the list of world's most ...",
              "source": "Tavily Search",
              "text": "Not just Venice is sinking! Here's the list of world's most .... Global warming and climate change are accelerating the rise of sea levels worldwide"
            },
            "similarity": 0.772,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_91feb6ef",
              "title": "Sea levels are rising faster than in 4000 years",
              "source": "Tavily Search",
              "text": "Sea levels are rising faster than in 4000 years. Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate cha"
            },
            "claim2": {
              "id": "tavily_6c8e05a9",
              "title": "Sea level rise cannot be pumped away - Frontline - The Hindu",
              "source": "Tavily Search",
              "text": "Sea level rise cannot be pumped away - Frontline - The Hindu. Under unabated warming, sea level rise may exceed 130 cm by 2100"
            },
            "similarity": 0.719,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_91feb6ef",
              "title": "Sea levels are rising faster than in 4000 years",
              "source": "Tavily Search",
              "text": "Sea levels are rising faster than in 4000 years. Global sea levels are rising at an alarming rate, unprecedented in 4,000 years, driven by climate cha"
            },
            "claim2": {
              "id": "tavily_b30ced11",
              "title": "Global sea level surging at faster rate, says study - Mint",
              "source": "Tavily Search",
              "text": "Global sea level surging at faster rate, says study - Mint. Washington: The global sea level is not rising at a steady rate, it is accelerating a litt"
            },
            "similarity": 0.781,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_624da5dd",
              "title": "Sea levels rising faster, Indian cities at high flood risk: IPCC",
              "source": "Tavily Search",
              "text": "Sea levels rising faster, Indian cities at high flood risk: IPCC. The report showed that the seas have actually risen globally by around 15cm during t"
            },
            "claim2": {
              "id": "tavily_bbf1b89b",
              "title": "Global sea level surging at faster rate: Study",
              "source": "Tavily Search",
              "text": "Global sea level surging at faster rate: Study. WASHINGTON: The global sea level is not rising at a steady rate, it is accelerating a little every yea"
            },
            "similarity": 0.784,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_624da5dd",
              "title": "Sea levels rising faster, Indian cities at high flood risk: IPCC",
              "source": "Tavily Search",
              "text": "Sea levels rising faster, Indian cities at high flood risk: IPCC. The report showed that the seas have actually risen globally by around 15cm during t"
            },
            "claim2": {
              "id": "tavily_3d26b3c1",
              "title": "Not just Venice is sinking! Here's the list of world's most ...",
              "source": "Tavily Search",
              "text": "Not just Venice is sinking! Here's the list of world's most .... Global warming and climate change are accelerating the rise of sea levels worldwide"
            },
            "similarity": 0.744,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_624da5dd",
              "title": "Sea levels rising faster, Indian cities at high flood risk: IPCC",
              "source": "Tavily Search",
              "text": "Sea levels rising faster, Indian cities at high flood risk: IPCC. The report showed that the seas have actually risen globally by around 15cm during t"
            },
            "claim2": {
              "id": "tavily_6c8e05a9",
              "title": "Sea level rise cannot be pumped away - Frontline - The Hindu",
              "source": "Tavily Search",
              "text": "Sea level rise cannot be pumped away - Frontline - The Hindu. Under unabated warming, sea level rise may exceed 130 cm by 2100"
            },
            "similarity": 0.743,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_624da5dd",
              "title": "Sea levels rising faster, Indian cities at high flood risk: IPCC",
              "source": "Tavily Search",
              "text": "Sea levels rising faster, Indian cities at high flood risk: IPCC. The report showed that the seas have actually risen globally by around 15cm during t"
            },
            "claim2": {
              "id": "tavily_b30ced11",
              "title": "Global sea level surging at faster rate, says study - Mint",
              "source": "Tavily Search",
              "text": "Global sea level surging at faster rate, says study - Mint. Washington: The global sea level is not rising at a steady rate, it is accelerating a litt"
            },
            "similarity": 0.784,
            "contradiction_type": "conflicting_claims"
          },
          {
            "claim1": {
              "id": "tavily_50a68002",
              "title": "Arabian Sea may rise by nearly 3ft over greenhouse effect",
              "source": "Tavily Search",
              "text": "Arabian Sea may rise by nearly 3ft over greenhouse effect. Global sea levels are rising because of human-caused global warming, with recent rates bein"
            },
            "claim2": {
              "id": "tavily_bbf1b89b",
              "title": "Global sea level surging at faster rate: Study",
              "source": "Tavily Search",
              "text": "Global sea level surging at faster rate: Study. WASHINGTON: The global sea level is not rising at a steady rate, it is accelerating a little every yea"
            },
            "similarity": 0.751,
            "contradiction_type": "conflicting_claims"
          }
        ],
        "risk_score": 1.0,
        "sample_contradictions": [
          "Fact-checkers debunk viral claim about government ... vs False rumors about food safety spread online, offi...",
          "Sea levels are rising faster than in 4000 years... vs Global sea level surging at faster rate: Study...",
          "Sea levels are rising faster than in 4000 years... vs Not just Venice is sinking! Here's the list of wor..."
        ],
        "total_datapoints": 81
      },
      "evolution_analysis": {
        "has_evolution": true,
        "evolution_stages": [
          {
            "window_index": 0,
            "time_range": {
              "start": "2025-01-15T06:30:00",
              "end": "2025-01-15T12:00:00"
            },
            "datapoint_count": 13,
            "key_phrases": [
              "about",
              "vaccine",
              "health",
              "safety",
              "social"
            ],
            "sample_titles": [
              "Rumors about water contamination prove unfounded",
              "Rumors about water contamination prove unfounded",
              "Government announces new health guidelines for public spaces"
            ]
          },
          {
            "window_index": 1,
            "time_range": {
              "start": "2025-01-15T16:00:00",
              "end": "2025-01-15T18:30:00"
            },
            "datapoint_count": 3,
            "key_phrases": [
              "health",
              "about",
              "updated",
              "public",
              "protocols"
            ],
            "sample_titles": [
              "Updated public health protocols released for indoor gatherings",
              "Fact-checkers debunk viral claim about government health measures",
              "False rumors about food safety spread online, officials clarify"
            ]
          },
          {
            "window_index": 2,
            "time_range": {
              "start": "2025-11-29T00:20:30.831000",
              "end": "2025-11-29T02:04:18.544000"
            },
            "datapoint_count": 65,
            "key_phrases": [
              "levels",
              "rise",
              "rising",
              "level",
              "global"
            ],
            "sample_titles": [
              "Latest News, Photos, Videos on India Weather",
              "Climate Change@ 2050: Why Mumbai may get that ' ...",
              "Mumbai climate risk: Greater awareness has reflected in ..."
            ]
          }
        ],
        "key_changes": [
          {
            "window": 1,
            "new_keywords": [
              "updated",
              "public",
              "protocols"
            ],
            "description": "Narrative shift detected: new focus on updated, public, protocols"
          },
          {
            "window": 2,
            "new_keywords": [
              "level",
              "levels",
              "rising",
              "rise",
              "global"
            ],
            "description": "Narrative shift detected: new focus on level, levels, rising"
          }
        ],
        "risk_score": 0.713,
        "total_stages": 3,
        "change_count": 2
      },
      "recommendation": "HIGH RISK: Immediate review recommended. Multiple red flags detected."
    }
  }
}


  const handleVerify = () => {
    if (!query.trim()) {
      setResult({
        title: "Please enter something to verify.",
        status: "-",
        summary: "-",
        explanation: "-",
        source: "-",
        confidence: "0%"
      });
      return;
    }
    // Always take public_updates[0]
    let key = Object.keys(mockData.classifications)[0]
    const first = key && mockData.classifications[key];
    if (!first) {
      setResult({
        title: "No updates available",
        status: "-",
        explanation: "-",
        source: "-",
        confidence: "0%"
      });
      return;
    }

    const title = mockData.prompt || "-";
    const status = first.classification || "-";
    const explanation = first.reasoning || "-";

    // choose first source URL if available
    const source = (first.sources && first.sources.length > 0) ? first.sources : [];

    // convert confidence to percentage (rounded)
    const confidencePct =
      typeof first.confidence === "number"
        ? `${Math.round(first.confidence * 100)}%`
        : "-";

    setResult({ title, status, explanation, source, confidence: confidencePct });
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

            <button
    onClick={handleClear}
    className="px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition"
  >
    Clear
  </button>
          </div>

          {/* Result Container */}
          <div className="mt-3 p-3 bg-gray-700 rounded-lg text-sm text-gray-200">
            {result && result.title === 'Please enter something to verify.' ? (
                <div>
                  <span>{result.title}</span>
                </div>
              ) : (
                ""
                )}
            {result && result.title === 'No updates available' ? (
                <div>
                  <span className="font-semibold">Title:</span>{" "}
                  <span>{result.title}</span>
                </div>
              ) : (
                ""
                )}
            {result && result.title !== 'No updates available' && result.title !== 'Please enter something to verify.' ? (
              <div className="space-y-2">
                <div>
                  <span className="font-semibold">Title:</span>{" "}
                  <span>{result.title}</span>
                </div>
                <div>
                  <span className="font-semibold">Status:</span>{" "}
                  <span className={`capitalize ${getStatusColor(result.status)}`}>{result.status}</span>
                </div>
                {/* <div>
                  <span className="font-semibold">Summary:</span>{" "}
                  <span>{result.summary}</span>
                </div> */}
                <div>
                  <span className="font-semibold">Explanation:</span>
                  <div className="mt-1 text-sm text-gray-300">{result.explanation}</div>
                </div>
                <div>
                <span className="font-semibold">Sources:</span>
                <ul className="list-disc ml-6 mt-1 space-y-1">
                  {result.source.length > 0 ? (
                    result.source.map((src, idx) => (
                      <li key={idx}>
                        <a
                          href={src}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="underline text-blue-300"
                        >
                          {src}
                        </a>
                      </li>
                    ))
                  ) : (
                    <li className="text-gray-400">No sources</li>
                  )}
                </ul>
              </div>
                <div>
                  <span className="font-semibold">Confidence:</span>{" "}
                  <span>{result.confidence}</span>
                </div>
              </div>
            ) : (
              "Result will appear here."
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
