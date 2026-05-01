export const site = {
  name: "Dooho Lee",
  tagline: "Researcher-builder working on foundation models for structured data.",
  email: "dooho@kaist.ac.kr",
  phone: "+82 (10) 6329 5955",
  location: "Daejeon, Republic of Korea",
  profilePhoto: "/profile.jpeg",
  cvHref: "/Dooho-Lee-CV.docx",
  scholar:
    "https://scholar.google.com/citations?user=Fv4CbSMAAAAJ&hl=en&oi=sra",
  linkedin: "https://www.linkedin.com/in/dooho-lee",
};

export const navItems = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  { label: "Research", href: "/research" },
  { label: "Projects", href: "/projects" },
  { label: "Experience", href: "/experience" },
  { label: "CV", href: "/cv" },
  { label: "Contact", href: "/contact" },
];

export const socialLinks = [
  { label: "Email", href: `mailto:${site.email}` },
  { label: "Google Scholar", href: site.scholar },
  { label: "LinkedIn", href: site.linkedin },
  { label: "GitHub", href: "", disabled: true },
];

export const education = [
  {
    degree: "M.S. in Electrical Engineering",
    institution: "KAIST",
    location: "Daejeon, Republic of Korea",
    period: "2025 - Present",
    detail: "Advised by Prof. Jaemin Yoo and Prof. Kijung Shin. GPA: 3.88.",
  },
  {
    degree: "B.S. in Electrical Engineering and Computer Science",
    institution: "KAIST",
    location: "Daejeon, Republic of Korea",
    period: "2019 - 2024",
    detail: "Double major. Graduated cum laude with GPA 3.77.",
  },
];

export const researchInterests = [
  "Graph Machine Learning",
  "Foundation Models",
  "Structured Data",
  "Predictive AI",
  "Time-Series Modeling",
  "Tabular Learning",
];
