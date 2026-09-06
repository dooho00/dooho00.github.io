# Dooho Lee Personal Website

Simple static academic homepage for Dooho Lee.

## Editing Content

Most content lives in `data/site.json`.

Install the PDF build dependency once:

```bash
python3 -m pip install -r requirements.txt
```

After editing the JSON, regenerate the homepage and CV together:

```bash
python3 build.py
```

This builds `index.html` and `CV_DoohoLee.pdf` from the same data and copies the
public files to `dist/`. The CV link downloads the generated PDF directly;
there is no print dialog or separate web CV page. PDF generation failures stop
the build. Source Serif 4 and Source Sans 3 are embedded in the PDF and hosted
locally for the website, with no external font request. Both use SIL OFL 1.1;
the original copyright notices and licenses ship in `assets/fonts/`.

## Local Preview

Open `index.html` directly in a browser.

## GitHub Pages

The Pages workflow builds both outputs before deploying `dist/` on pushes to
`main`. When promoting the preview to GitHub, select **Settings -> Pages ->
Build and deployment -> Source -> GitHub Actions** once. Until then the existing
GitHub homepage is unchanged. Generated root files can still be opened locally.

For the private Sites preview, run `python3 build.py` before packaging `dist/`.
