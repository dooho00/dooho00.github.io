export type Project = {
  name: string;
  tagline: string;
  problem: string;
  built: string;
  role: string;
  technologies: string[];
  outcome: string;
};

export const projects: Project[] = [
  {
    name: "Pensieve Extension",
    tagline: "LLM-powered Chrome highlight note-taking.",
    problem:
      "Researchers and knowledge workers highlight useful text but often lose the surrounding reasoning context.",
    built:
      "A Chrome extension that turns browser highlights into structured, real-time notes powered by LLM workflows.",
    role: "Founding Engineer & Designer at Pensieve Inc.",
    technologies: ["LLMs", "Chrome Extensions", "TypeScript", "Product Design"],
    outcome:
      "Built as part of Pensieve's subscription software suite and contributed to early revenue.",
  },
  {
    name: "Pensieve Notes",
    tagline: "Zoom transcription and automatic meeting notes.",
    problem:
      "Teams need reliable meeting memory without manually writing notes during calls.",
    built:
      "A Zoom transcription product that generates meeting notes automatically from live conversations.",
    role: "Founding Engineer & Designer at Pensieve Inc.",
    technologies: ["LLMs", "Zoom Apps", "Transcription", "React"],
    outcome: "Served 3 organizations through early deployments.",
  },
  {
    name: "WARD",
    tagline: "ML-based stock information service.",
    problem:
      "Individual investors need clearer signals and information structure in crowded financial data.",
    built:
      "A machine-learning stock information service with user research loops for fund managers and beta users.",
    role: "Co-Founder, Software Engineer & Designer",
    technologies: ["Machine Learning", "Finance Data", "Web", "UX Research"],
    outcome:
      "Launched private beta with 200+ users and was selected as a top 12 team in KAIST E*5.",
  },
  {
    name: "LayUs",
    tagline: "Exhibition ticket-based F&B coupon redemption.",
    problem:
      "Exhibition visitors and venues need a lightweight way to connect admission proof with nearby benefits.",
    built:
      "A mobile app where users upload exhibition tickets and redeem food-and-beverage coupons.",
    role: "Software Engineer",
    technologies: ["Mobile App", "Product Design", "Ticket Verification"],
    outcome: "Awarded 2nd place in an Art Service follow-up growth support project.",
  },
];
