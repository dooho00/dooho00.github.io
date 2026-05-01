export type Publication = {
  title: string;
  authors: string;
  venue: string;
  year: string;
  summary: string;
  tags: string[];
  featured?: boolean;
  links: Array<{
    label: "Paper" | "Code" | "Project";
    href?: string;
    disabled?: boolean;
  }>;
};

export const publications: Publication[] = [
  {
    title: "View Space: Learning Representation across Arbitrary Graphs",
    authors: "Dooho Lee, Myeong Kong, Minho Jeong, and Jaemin Yoo",
    venue: "International Conference on Machine Learning (ICML)",
    year: "2026",
    summary:
      "A graph representation learning direction for models that can transfer across heterogeneous graph datasets and structural views.",
    tags: ["Graph ML", "Foundation Models", "Representation Learning"],
    featured: true,
    links: [
      { label: "Paper", disabled: true },
      { label: "Code", disabled: true },
      { label: "Project", disabled: true },
    ],
  },
  {
    title: "Generalizing Multi-Scale Time-Series Modeling with a Single Operator",
    authors: "Cheonwoo Lee, Dooho Lee, Doyun Choi, and Jaemin Yoo",
    venue: "International Conference on Machine Learning (ICML)",
    year: "2025",
    summary:
      "A unified operator for multi-scale time-series modeling, focused on generalization across temporal resolutions and datasets.",
    tags: ["Time Series", "Generalization", "Predictive AI"],
    featured: true,
    links: [
      { label: "Paper", disabled: true },
      { label: "Code", disabled: true },
      { label: "Project", disabled: true },
    ],
  },
  {
    title: "Aggregation Buffer: Revisiting DropEdge with a New Parameter Block",
    authors: "Dooho Lee, Myeong Kong, Sagad Hamid, Cheonwoo Lee, and Jaemin Yoo",
    venue: "International Conference on Machine Learning (ICML)",
    year: "2025",
    summary:
      "A graph neural network training method that revisits DropEdge through a parameterized aggregation buffer.",
    tags: ["Graph ML", "GNNs", "Robust Training"],
    featured: true,
    links: [
      { label: "Paper", disabled: true },
      { label: "Code", disabled: true },
      { label: "Project", disabled: true },
    ],
  },
];

export const researchThemes = [
  {
    title: "Graph Foundation Models",
    text: "Learning representations that transfer across arbitrary graph structures, domains, and tasks.",
  },
  {
    title: "Generalization Across Datasets",
    text: "Building models that remain useful when the data schema, scale, or distribution changes.",
  },
  {
    title: "Structured-Data Prediction",
    text: "Predictive AI for graph, time-series, and tabular data where relationships carry the signal.",
  },
  {
    title: "Learning with Synthetic Data",
    text: "Using controllable generated data to probe model behavior and improve transfer.",
  },
  {
    title: "World Models for Prediction",
    text: "Moving beyond language-only intelligence toward models that understand real-world structure.",
  },
];
