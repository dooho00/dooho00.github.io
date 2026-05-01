export type TimelineEntry = {
  title: string;
  organization: string;
  location?: string;
  period: string;
  category: "Startup" | "Research" | "Service" | "Military";
  summary: string;
  highlights: string[];
  tags: string[];
};

export const experienceTimeline: TimelineEntry[] = [
  {
    title: "Research Project",
    organization: "National Cyber Security Research Institute",
    location: "Republic of Korea",
    period: "Jan 2025 - Feb 2026",
    category: "Research",
    summary: "Graph-based tracking of news propagation on social media using LLMs.",
    highlights: [
      "Worked on graph-based modeling for social media news propagation.",
      "Connected LLM-driven analysis with structured propagation signals.",
    ],
    tags: ["Graphs", "LLMs", "Social Media"],
  },
  {
    title: "Undergraduate Intern",
    organization: "DataAI Lab, KAIST",
    location: "Daejeon, KR",
    period: "Jan 2024 - Feb 2025",
    category: "Research",
    summary: "Studied traditional and recent advances in graph machine learning.",
    highlights: [
      "Conducted focused study of graph learning methods.",
      "Built the research base that led into structured-data foundation model work.",
    ],
    tags: ["Graph ML", "Research"],
  },
  {
    title: "Undergraduate Intern",
    organization: "MultiModalAI Lab, KAIST",
    location: "Daejeon, KR",
    period: "Aug 2023 - Dec 2023",
    category: "Research",
    summary: "Studied foundational deep learning papers in computer vision and multimodality.",
    highlights: [
      "Reviewed core papers across computer vision and multimodal learning.",
      "Expanded modeling perspective beyond single-modality pipelines.",
    ],
    tags: ["Deep Learning", "Multimodal AI"],
  },
  {
    title: "Founding Engineer & Designer",
    organization: "Pensieve Inc.",
    location: "Berkeley, CA",
    period: "Nov 2022 - Aug 2023",
    category: "Startup",
    summary: "Co-founded a US startup with two UC Berkeley students building LLM software.",
    highlights: [
      "Built LLM-powered software products including Chrome highlight notes and Zoom meeting notes.",
      "Generated profit through software subscription fees and sales revenue.",
    ],
    tags: ["LLMs", "Chrome", "Zoom", "Design"],
  },
  {
    title: "KATUSA",
    organization: "US Army",
    location: "USAG Humphreys, KR",
    period: "Nov 2021 - May 2023",
    category: "Military",
    summary: "Korean Augmentation to the United States Army.",
    highlights: [
      "Supported US-KR communication in Bravo Company, 602nd ASB, 2nd CAB, 2nd ID.",
      "Served as the only KATUSA in the largest company of the US Army unit.",
    ],
    tags: ["Communication", "Operations"],
  },
  {
    title: "Software Engineer",
    organization: "LayUs",
    location: "Seoul, KR",
    period: "Mar 2022 - Jul 2022",
    category: "Startup",
    summary: "Built a mobile application for exhibition ticket-based F&B coupon redemption.",
    highlights: [
      "Implemented a ticket upload flow for coupon eligibility.",
      "Helped connect exhibition visitors with local benefits through mobile UX.",
    ],
    tags: ["Mobile", "Product"],
  },
  {
    title: "Co-Founder, Software Engineer & Designer",
    organization: "WARD",
    period: "Sep 2020 - Oct 2021",
    category: "Startup",
    summary: "Co-founded a machine-learning stock information service.",
    highlights: [
      "Selected as a top 12 team in 2021 E*5 KAIST under Blue Point Partners mentorship.",
      "Launched a private beta with 200+ users and ran fund manager sessions, interviews, and surveys.",
    ],
    tags: ["ML", "Finance", "Design"],
  },
];

export const teaching = [
  {
    role: "TA, Programming Structures for Electrical Engineering",
    course: "EE209, KAIST",
    period: "2025 Spring, Fall",
    detail:
      "Independently developed a data structures programming assignment with auto-grading for a core course serving 200+ EE majors each semester.",
  },
  {
    role: "TA, Foundation of Big Data Analytics",
    course: "EE412, KAIST",
    period: "2025 Fall",
    detail: "Teaching assistant for KAIST big data analytics coursework.",
  },
];

export const service = [
  {
    title: "Reviewer",
    organization: "NeurIPS",
    period: "2026",
  },
  {
    title: "Invited Research Talk",
    organization: "Korea Software Congress 2025",
    period: "Dec 2025",
    href: "https://www.kiise.or.kr/conference/KSC/2025/",
  },
];
