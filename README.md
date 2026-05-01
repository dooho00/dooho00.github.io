# Dooho Lee Personal Website

Simple academic personal homepage for Dooho Lee, built with React, Vite, and plain CSS.

## Development

```bash
npm install
npm run dev
```

## Production Build

```bash
npm run build
npm run preview
```

Content is organized in `src/data` so publications, projects, experience, skills, and awards can be updated without rewriting the page.

## GitHub Pages Without Actions

This repository can be published without GitHub Actions by committing the built static files in `docs/`.

```bash
npm run build
mkdir -p docs
cp -R dist/. docs/
git add -A
git commit -m "Build simplified academic homepage"
git push origin main
```

In GitHub, set `Settings -> Pages -> Deploy from a branch`, then choose `main` and `/docs`.
