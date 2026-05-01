export type SkillGroup = {
  title: string;
  skills: string[];
};

export const skillGroups: SkillGroup[] = [
  {
    title: "Research",
    skills: [
      "Graph Machine Learning",
      "Foundation Models",
      "Time-Series Modeling",
      "Tabular Learning",
      "Predictive AI",
      "Representation Learning",
    ],
  },
  {
    title: "Machine Learning",
    skills: ["PyTorch", "PyTorch Geometric", "DGL", "Weights & Biases"],
  },
  {
    title: "Programming",
    skills: ["Python", "C", "C++", "Java", "JavaScript", "TypeScript"],
  },
  {
    title: "Front-End & UI",
    skills: ["HTML", "CSS", "Tailwind CSS", "React", "React Native", "Flutter"],
  },
  {
    title: "Back-End & Data",
    skills: ["MySQL", "Neo4j", "Chroma", "Firebase", "Google Cloud Platform"],
  },
  {
    title: "Design & Tools",
    skills: ["Figma", "Adobe XD", "Adobe Illustrator", "Git", "Chrome Extensions", "Zoom Apps"],
  },
  {
    title: "Languages",
    skills: ["Korean", "English"],
  },
];
