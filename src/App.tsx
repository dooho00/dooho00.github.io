import { awards } from "./data/awards";
import { experienceTimeline, service, teaching } from "./data/experience";
import { projects } from "./data/projects";
import { publications } from "./data/publications";
import { education, researchInterests, site } from "./data/site";
import { skillGroups } from "./data/skills";

const navItems = [
  ["About", "#about"],
  ["Publications", "#publications"],
  ["Projects", "#projects"],
  ["Experience", "#experience"],
  ["Honors", "#honors"],
  ["Teaching", "#teaching"],
  ["Service", "#service"],
];

function Section({
  id,
  title,
  children,
}: {
  id: string;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="section">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function ExternalLink({
  href,
  children,
  download,
}: {
  href: string;
  children: React.ReactNode;
  download?: boolean;
}) {
  return (
    <a
      href={href}
      target={href.startsWith("http") ? "_blank" : undefined}
      rel={href.startsWith("http") ? "noreferrer" : undefined}
      download={download}
    >
      {children}
    </a>
  );
}

export default function App() {
  const awardsByCategory = awards.reduce<Record<string, typeof awards>>((groups, award) => {
    groups[award.category] = groups[award.category] ? [...groups[award.category], award] : [award];
    return groups;
  }, {});

  return (
    <div className="site-shell">
      <header className="profile">
        <img src={site.profilePhoto} alt="Dooho Lee" />
        <div>
          <h1>Dooho Lee</h1>
          <p className="role">M.S. Student, KAIST Electrical Engineering</p>
          <p className="tagline">I build foundation models for structured data.</p>
          <div className="links" aria-label="Profile links">
            <ExternalLink href={`mailto:${site.email}`}>Email</ExternalLink>
            <ExternalLink href={site.scholar}>Google Scholar</ExternalLink>
            <ExternalLink href={site.linkedin}>LinkedIn</ExternalLink>
            <ExternalLink href={site.cvHref} download>
              CV
            </ExternalLink>
          </div>
        </div>
      </header>

      <nav className="anchor-nav" aria-label="Section navigation">
        {navItems.map(([label, href]) => (
          <a key={href} href={href}>
            {label}
          </a>
        ))}
      </nav>

      <main>
        <Section id="about" title="About">
          <p>
            I am a second-year M.S. student in Electrical Engineering at KAIST, advised by Prof. Jaemin Yoo and Prof.
            Kijung Shin. My research focuses on machine learning for structured data, including graphs, time series, and
            tabular data, with a recent focus on foundation models.
          </p>
          <p>
            Outside academia, I have co-founded and worked as a software engineer and designer in multiple startups,
            building products around LLM-powered workflows, finance, and mobile applications.
          </p>
          <div className="chips">
            {researchInterests.map((interest) => (
              <span key={interest}>{interest}</span>
            ))}
          </div>
        </Section>

        <Section id="news" title="News">
          <ul className="simple-list">
            <li>
              <strong>2026</strong> - View Space accepted to ICML 2026.
            </li>
            <li>
              <strong>2025</strong> - Two papers accepted to ICML 2025.
            </li>
            <li>
              <strong>2025</strong> - Invited research talk at Korea Software Congress 2025.
            </li>
          </ul>
        </Section>

        <Section id="publications" title="Publications">
          <div className="publication-list">
            {publications.map((publication) => (
              <article key={publication.title} className="publication">
                <div className="pub-year">{publication.year}</div>
                <div>
                  <h3>{publication.title}</h3>
                  <p className="authors">{publication.authors}</p>
                  <p className="venue">
                    {publication.venue}, {publication.year}
                  </p>
                  <div className="chips compact">
                    {publication.tags.map((tag) => (
                      <span key={tag}>{tag}</span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>
        </Section>

        <Section id="projects" title="Projects">
          <div className="card-grid">
            {projects.map((project) => (
              <article key={project.name} className="mini-card">
                <h3>{project.name}</h3>
                <p className="muted">{project.tagline}</p>
                <p>{project.built}</p>
                <p className="small">
                  <strong>Role:</strong> {project.role}
                </p>
                <p className="small">
                  <strong>Impact:</strong> {project.outcome}
                </p>
              </article>
            ))}
          </div>
        </Section>

        <Section id="experience" title="Experience">
          <div className="timeline">
            {education.map((item) => (
              <article key={item.degree} className="timeline-row">
                <div className="date">{item.period}</div>
                <div>
                  <h3>{item.degree}</h3>
                  <p>
                    {item.institution}, {item.location}
                  </p>
                  <p className="muted">{item.detail}</p>
                </div>
              </article>
            ))}
            {experienceTimeline.map((entry) => (
              <article key={`${entry.organization}-${entry.period}`} className="timeline-row">
                <div className="date">{entry.period}</div>
                <div>
                  <h3>
                    {entry.title}, {entry.organization}
                  </h3>
                  <p className="muted">{entry.summary}</p>
                </div>
              </article>
            ))}
          </div>
        </Section>

        <Section id="skills" title="Skills">
          <div className="skill-list">
            {skillGroups.map((group) => (
              <p key={group.title}>
                <strong>{group.title}:</strong> {group.skills.join(", ")}
              </p>
            ))}
          </div>
        </Section>

        <Section id="honors" title="Awards & Honors">
          <div className="card-grid two">
            {Object.entries(awardsByCategory).map(([category, items]) => (
              <article key={category} className="mini-card">
                <h3>{category}</h3>
                <ul className="simple-list">
                  {items.map((award) => (
                    <li key={award.title}>
                      {award.title} <span className="date-inline">{award.date}</span>
                    </li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        </Section>

        <Section id="teaching" title="Teaching">
          <div className="timeline">
            {teaching.map((item) => (
              <article key={item.role} className="timeline-row">
                <div className="date">{item.period}</div>
                <div>
                  <h3>{item.role}</h3>
                  <p>{item.course}</p>
                  <p className="muted">{item.detail}</p>
                </div>
              </article>
            ))}
          </div>
        </Section>

        <Section id="service" title="Professional Service">
          <ul className="simple-list">
            {service.map((item) => (
              <li key={`${item.title}-${item.organization}`}>
                {item.title}, {item.href ? <ExternalLink href={item.href}>{item.organization}</ExternalLink> : item.organization} (
                {item.period})
              </li>
            ))}
          </ul>
        </Section>
      </main>

      <footer>
        <p>
          Dooho Lee · <ExternalLink href={`mailto:${site.email}`}>{site.email}</ExternalLink>
        </p>
      </footer>
    </div>
  );
}
