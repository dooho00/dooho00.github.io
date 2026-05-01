export type Award = {
  title: string;
  category: "Startup" | "Design" | "Other";
  date: string;
};

export const awards: Award[] = [
  {
    title: "2nd place, 2023 Korea SW Startup Ideathon (Team Fall-Asleep)",
    category: "Startup",
    date: "Oct 2023",
  },
  {
    title: "1st place, Pre-Startup Package, Daejeon Center for Creative Economy and Innovation",
    category: "Startup",
    date: "Aug 2021",
  },
  {
    title: "1st place, 8th Army ROKA Support Group Insignia Competition",
    category: "Design",
    date: "Apr 2023",
  },
  {
    title: "2nd place, Art Service Follow-up Growth Support Project (Team LayUs)",
    category: "Design",
    date: "Nov 2022",
  },
  {
    title: "2024 Team KAIST Global Challenge Program, $15,000 funding",
    category: "Other",
    date: "Apr 2023",
  },
  {
    title: "Bronze Medal, NH Investment Securities Big Data Competition (Team WARD)",
    category: "Other",
    date: "Aug 2021",
  },
  {
    title: "1st place, 7th Creative Space G A.I & IoT Hackathon",
    category: "Other",
    date: "Jul 2021",
  },
];
