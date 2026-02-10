# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pelican-based personal blog hosted on GitHub Pages at tybug.dev.

## Build & Serve

```bash
pip install -r requirements.txt       # Install Python dependencies
pelican --listen                       # Build and serve at http://127.0.0.1:8000/
```

Deployment is via GitHub Actions on push to master.

## Architecture

- **`content/articles/`** — Blog posts in Markdown with Pelican metadata header (Title, Date, Tags, Slug, etc.).
- **`content/pages/`** — Static pages (e.g., `contracting.html`).
- **`content/extra/`** — Files copied as-is to output (CNAME, PDF).
- **`theme/templates/`** — Jinja2 templates: `base.html` (shell), `article.html` (post), `index.html` (home), `tag.html` (tag listing), `page.html` (static pages).
- **`theme/static/css/`** — SCSS source files, compiled to CSS at build time by the webassets plugin.
- **`theme/static/js/mathjax/`** — Vendored MathJax for LaTeX math rendering.
- **`plugins/`** — Custom Pelican plugins: `validate_articles.py` (date check), `hidden_articles.py` (hide from listings), `redirect_generator.py` (old URL redirects).
- **`pelicanconf.py`** — Dev config. **`publishconf.py`** — Production config (sets SITEURL).

## Article Metadata

```
Title: Post Title
Date: 2024-01-15
Tags: python, math
Slug: post-slug
```

Optional: `Hidden: true` (accessible but unlisted), `Status: draft` (not published).

## Key Conventions

- MathJax is enabled globally: use `$...$` for inline math, `$$...$$` for display math (via pymdownx.arithmatex).
- Python-Markdown with footnotes, fenced_code, codehilite, tables extensions.
- No JavaScript frameworks — plain HTML/CSS with minimal JS (only MathJax).
