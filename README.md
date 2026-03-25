# HireLens

HireLens is a portfolio-ready data analytics project that analyzes analyst and BI hiring demand, compares it with a candidate profile, and turns the gap into a focused upskilling roadmap.

## Overview

The goal of this project is to answer a practical career question:

Which analyst roles best match the current profile, and which skills should be learned next to become more competitive in the market?

To answer that, HireLens combines:

- a structured local job-market dataset
- a Python pipeline for analysis and transformation
- SQLite for queryable role and skill analysis
- a polished frontend dashboard for storytelling

## What This Project Does

- models analyst and BI job postings across major Indian cities
- stores raw and normalized data in CSV and SQLite formats
- analyzes role demand, city clusters, work mode, salary patterns, and top skills
- compares current skills against market demand for target roles
- identifies strongest-fit roles and highest-priority skill gaps
- generates a three-month upskilling roadmap

## Current Output Highlights

From the current generated analysis:

- `180` job postings were modeled in the local dataset
- `16` companies are represented in the sample
- `BI Analyst` appears as the strongest-fit target role
- `Power BI` is the highest-value skill gap to close next

## Tech Stack

- `Python`
- `SQL`
- `SQLite`
- `HTML`
- `CSS`
- `JavaScript`

## Project Structure

- `config/profile.json`
  Candidate profile, current skills, and target roles used for gap analysis
- `scripts/build_pipeline.py`
  Generates the dataset, builds the SQLite database, calculates insights, and exports dashboard-ready outputs
- `data/raw/job_postings.csv`
  Generated job posting dataset
- `data/processed/job_market.db`
  SQLite database for structured querying
- `data/processed/analysis.json`
  Final analysis output used by the dashboard
- `dashboard/index.html`
  Portfolio-style frontend
- `dashboard/styles.css`
  Visual design and layout
- `dashboard/app.js`
  Rendering logic for cards, charts, tables, and roadmap
- `sql/market_queries.sql`
  Reusable SQL analysis queries

## How It Works

1. A synthetic dataset of analyst and BI roles is generated with fields such as title, city, company, salary, experience band, and required skills.
2. The dataset is loaded into SQLite and normalized into job and skill tables.
3. The current profile from `config/profile.json` is compared against market demand.
4. Role-fit scores, skill-gap priorities, and market insights are calculated.
5. The outputs are exported into JSON and dashboard-ready JavaScript.
6. A static frontend presents the final story in a recruiter-friendly way.

## Run The Pipeline

```powershell
python scripts/build_pipeline.py
```

## Open The Dashboard

Open `dashboard/index.html` directly in a browser, or serve the folder locally:

```powershell
python -m http.server 8000 -d dashboard
```

Then visit `http://localhost:8000`.

## Customization

To personalize the analysis, edit:

- `config/profile.json`

You can change:

- target roles
- current skills
- learning goal

Then rerun the pipeline to regenerate the outputs.

## Suggested Next Upgrades

- replace the synthetic dataset with scraped or manually collected job-board data
- add filters by city, role, and experience level
- extend the pipeline with resume parsing and keyword matching
- convert the dashboard into a deployable React or Next.js app
- publish the project with screenshots and a hosted live demo
