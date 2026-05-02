# Dooho Lee Personal Website

Simple static academic homepage for Dooho Lee.

## Editing Content

Most content lives in `data/site.json`.

After editing the JSON, regenerate the homepage:

```bash
python3 build.py
```

## Local Preview

Open `index.html` directly in a browser.

## GitHub Pages

This site does not require Node, npm, or GitHub Actions. Commit the generated `index.html` together with the JSON changes.

Recommended setting:

```text
Settings -> Pages -> Deploy from a branch -> main -> /root
```
