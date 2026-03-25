from __future__ import annotations

import csv
import json
import random
import sqlite3
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
CONFIG_DIR = ROOT / "config"
DASHBOARD_DIR = ROOT / "dashboard"

CSV_PATH = RAW_DIR / "job_postings.csv"
DB_PATH = PROCESSED_DIR / "job_market.db"
ANALYSIS_PATH = PROCESSED_DIR / "analysis.json"
DASHBOARD_DATA_PATH = DASHBOARD_DIR / "analysis-data.js"
PROFILE_PATH = CONFIG_DIR / "profile.json"

RANDOM = random.Random(42)
TODAY = date(2026, 3, 24)

ROLE_PROFILES = {
    "Data Analyst": {
        "titles": ["Data Analyst", "Junior Data Analyst", "Data Analyst - Reporting"],
        "base_salary_lpa": 6.2,
        "skill_weights": {
            "SQL": 0.95,
            "Excel": 0.88,
            "Power BI": 0.72,
            "Python": 0.64,
            "Data Cleaning": 0.58,
            "Dashboarding": 0.60,
            "Statistics": 0.44,
            "Communication": 0.47,
            "Stakeholder Management": 0.32,
            "ETL": 0.31,
            "A/B Testing": 0.20,
            "Tableau": 0.26,
        },
    },
    "BI Analyst": {
        "titles": ["BI Analyst", "Business Intelligence Analyst", "BI Reporting Analyst"],
        "base_salary_lpa": 7.4,
        "skill_weights": {
            "SQL": 0.92,
            "Power BI": 0.90,
            "Excel": 0.67,
            "Dashboarding": 0.82,
            "DAX": 0.58,
            "Power Query": 0.51,
            "Data Modeling": 0.55,
            "ETL": 0.44,
            "Communication": 0.42,
            "Stakeholder Management": 0.39,
            "Python": 0.34,
            "Tableau": 0.18,
        },
    },
    "Power BI Analyst": {
        "titles": ["Power BI Analyst", "Power BI Developer", "Reporting Analyst - Power BI"],
        "base_salary_lpa": 7.9,
        "skill_weights": {
            "Power BI": 0.98,
            "SQL": 0.90,
            "DAX": 0.80,
            "Power Query": 0.71,
            "Excel": 0.62,
            "Data Modeling": 0.59,
            "Dashboarding": 0.79,
            "ETL": 0.42,
            "Communication": 0.33,
            "Stakeholder Management": 0.28,
            "Python": 0.20,
        },
    },
    "Reporting Analyst": {
        "titles": ["Reporting Analyst", "MIS Analyst", "Operations Reporting Analyst"],
        "base_salary_lpa": 5.8,
        "skill_weights": {
            "Excel": 0.94,
            "SQL": 0.76,
            "Power BI": 0.62,
            "Dashboarding": 0.55,
            "Communication": 0.45,
            "Stakeholder Management": 0.37,
            "Power Query": 0.31,
            "Python": 0.22,
            "Data Cleaning": 0.49,
            "Tableau": 0.16,
        },
    },
    "Business Analyst": {
        "titles": ["Business Analyst", "Business Analyst - Analytics", "Insights Analyst"],
        "base_salary_lpa": 7.0,
        "skill_weights": {
            "SQL": 0.74,
            "Excel": 0.71,
            "Power BI": 0.52,
            "Communication": 0.73,
            "Stakeholder Management": 0.61,
            "Dashboarding": 0.42,
            "Python": 0.29,
            "A/B Testing": 0.25,
            "Statistics": 0.24,
            "Documentation": 0.46,
        },
    },
}

CITIES = [
    ("New Delhi", 1.35),
    ("Gurugram", 1.30),
    ("Noida", 1.22),
    ("Bengaluru", 1.20),
    ("Pune", 0.98),
    ("Mumbai", 0.92),
    ("Hyderabad", 0.90),
]

INDUSTRIES = [
    "E-commerce",
    "FinTech",
    "SaaS",
    "Consulting",
    "Retail",
    "Healthcare",
    "Logistics",
    "EdTech",
]

WORK_MODES = [
    ("On-site", 0.44),
    ("Hybrid", 0.38),
    ("Remote", 0.18),
]

EXPERIENCE_LEVELS = {
    "Intern": {"weight": 0.10, "min_exp": 0, "max_exp": 0, "salary_factor": 0.58},
    "Entry": {"weight": 0.46, "min_exp": 0, "max_exp": 2, "salary_factor": 0.82},
    "Mid": {"weight": 0.29, "min_exp": 2, "max_exp": 5, "salary_factor": 1.12},
    "Senior": {"weight": 0.15, "min_exp": 5, "max_exp": 8, "salary_factor": 1.48},
}

COMPANIES = [
    "Acumen Retail",
    "NexaPulse",
    "BlueOrbit Analytics",
    "MetricHive",
    "TrueNorth Commerce",
    "Verity Health",
    "UrbanCart",
    "SignalCraft",
    "LedgerLoop",
    "BrightLane Logistics",
    "ScalePoint",
    "DataNook Consulting",
    "HelioMetrics",
    "PrimeBasket",
    "InsightForge",
    "FlowGrid",
]

SKILL_ALIASES = {
    "exploratory data analysis": "EDA",
    "kpi reporting": "KPI Reporting",
    "stakeholder communication": "Stakeholder Management",
    "mysql": "SQL",
    "sqlite": "SQL",
}


def weighted_choice(weight_map: dict[str, float]) -> str:
    keys = list(weight_map.keys())
    weights = list(weight_map.values())
    return RANDOM.choices(keys, weights=weights, k=1)[0]


def weighted_choice_list(items: list[tuple[str, float]]) -> str:
    keys = [item[0] for item in items]
    weights = [item[1] for item in items]
    return RANDOM.choices(keys, weights=weights, k=1)[0]


def normalize_skill(skill: str) -> str:
    return SKILL_ALIASES.get(skill.strip().lower(), skill.strip())


def generate_skills(role_name: str, exp_level: str) -> list[str]:
    profile = ROLE_PROFILES[role_name]["skill_weights"]
    skills: list[str] = []

    for skill, probability in profile.items():
        adjusted = probability
        if exp_level == "Intern" and skill in {"DAX", "Power Query", "Data Modeling", "ETL"}:
            adjusted *= 0.65
        if exp_level == "Senior" and skill in {"Stakeholder Management", "Communication", "ETL"}:
            adjusted *= 1.15
        if RANDOM.random() < min(adjusted, 0.98):
            skills.append(skill)

    if "SQL" not in skills and RANDOM.random() < 0.78:
        skills.append("SQL")
    if role_name in {"BI Analyst", "Power BI Analyst"} and "Power BI" not in skills:
        skills.append("Power BI")
    if role_name == "Power BI Analyst" and "DAX" not in skills and RANDOM.random() < 0.72:
        skills.append("DAX")

    filler_pool = [
        "Excel",
        "Communication",
        "Dashboarding",
        "SQL",
        "Python",
        "Power BI",
        "Data Cleaning",
        "Documentation",
    ]
    while len(skills) < 6:
        filler = RANDOM.choice(filler_pool)
        if filler not in skills:
            skills.append(filler)

    RANDOM.shuffle(skills)
    return skills[:8]


def build_description(role_name: str, skills: list[str], city: str) -> str:
    focus = ", ".join(skills[:4])
    return (
        f"Support business teams in {city} by turning raw operational data into decision-ready insights. "
        f"The role emphasizes {focus} and strong reporting discipline."
    )


def generate_job_rows(total_rows: int = 180) -> list[dict[str, object]]:
    role_weights = {
        "Data Analyst": 0.30,
        "BI Analyst": 0.24,
        "Power BI Analyst": 0.18,
        "Reporting Analyst": 0.16,
        "Business Analyst": 0.12,
    }

    rows = []
    for index in range(1, total_rows + 1):
        role_name = weighted_choice(role_weights)
        city = weighted_choice_list(CITIES)
        industry = RANDOM.choice(INDUSTRIES)
        work_mode = weighted_choice_list(WORK_MODES)
        exp_level = weighted_choice({key: value["weight"] for key, value in EXPERIENCE_LEVELS.items()})
        exp_config = EXPERIENCE_LEVELS[exp_level]
        title = RANDOM.choice(ROLE_PROFILES[role_name]["titles"])
        company = RANDOM.choice(COMPANIES)
        posted_date = TODAY - timedelta(days=RANDOM.randint(1, 75))
        skills = generate_skills(role_name, exp_level)

        base_salary = ROLE_PROFILES[role_name]["base_salary_lpa"] * exp_config["salary_factor"]
        city_factor = dict(CITIES)[city]
        salary_lpa = round(base_salary * (0.88 + RANDOM.random() * 0.26) * (0.90 + (city_factor - 0.9) * 0.18), 1)

        rows.append(
            {
                "job_id": f"JG-{index:03d}",
                "title": title,
                "role_name": role_name,
                "company": company,
                "city": city,
                "work_mode": work_mode,
                "experience_level": exp_level,
                "min_experience": exp_config["min_exp"],
                "max_experience": exp_config["max_exp"],
                "industry": industry,
                "salary_lpa": salary_lpa,
                "posted_date": posted_date.isoformat(),
                "skills": "|".join(skills),
                "description": build_description(role_name, skills, city),
            }
        )
    return rows


def write_csv(rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys())
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_profile() -> dict[str, object]:
    with PROFILE_PATH.open(encoding="utf-8") as handle:
        profile = json.load(handle)
    profile["normalized_skills"] = sorted({normalize_skill(skill) for skill in profile["current_skills"]})
    return profile


def build_database(rows: list[dict[str, object]]) -> sqlite3.Connection:
    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE job_postings (
            job_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            role_name TEXT NOT NULL,
            company TEXT NOT NULL,
            city TEXT NOT NULL,
            work_mode TEXT NOT NULL,
            experience_level TEXT NOT NULL,
            min_experience INTEGER NOT NULL,
            max_experience INTEGER NOT NULL,
            industry TEXT NOT NULL,
            salary_lpa REAL NOT NULL,
            posted_date TEXT NOT NULL,
            skills TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE job_skills (
            job_id TEXT NOT NULL,
            role_name TEXT NOT NULL,
            city TEXT NOT NULL,
            skill TEXT NOT NULL,
            FOREIGN KEY(job_id) REFERENCES job_postings(job_id)
        )
        """
    )
    cursor.executemany(
        """
        INSERT INTO job_postings (
            job_id, title, role_name, company, city, work_mode, experience_level,
            min_experience, max_experience, industry, salary_lpa, posted_date, skills, description
        ) VALUES (
            :job_id, :title, :role_name, :company, :city, :work_mode, :experience_level,
            :min_experience, :max_experience, :industry, :salary_lpa, :posted_date, :skills, :description
        )
        """,
        rows,
    )

    skill_rows = []
    for row in rows:
        for skill in row["skills"].split("|"):
            skill_rows.append(
                {
                    "job_id": row["job_id"],
                    "role_name": row["role_name"],
                    "city": row["city"],
                    "skill": normalize_skill(skill),
                }
            )
    cursor.executemany(
        """
        INSERT INTO job_skills (job_id, role_name, city, skill)
        VALUES (:job_id, :role_name, :city, :skill)
        """,
        skill_rows,
    )
    connection.commit()
    return connection


def query_pairs(connection: sqlite3.Connection, sql: str, limit: int = 999) -> list[dict[str, object]]:
    cursor = connection.cursor()
    cursor.execute(sql)
    return [{"label": row[0], "value": row[1]} for row in cursor.fetchmany(limit)]


def compute_role_fit(connection: sqlite3.Connection, profile_skills: set[str]) -> list[dict[str, object]]:
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT role_name, skill, COUNT(*) AS demand
        FROM job_skills
        GROUP BY role_name, skill
        ORDER BY role_name, demand DESC
        """
    )

    grouped: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for role_name, skill, demand in cursor.fetchall():
        grouped[role_name].append((skill, demand))

    fit_scores = []
    for role_name, skill_rows in grouped.items():
        top_skills = skill_rows[:8]
        total_weight = sum(weight for _, weight in top_skills)
        matched_weight = sum(weight for skill, weight in top_skills if skill in profile_skills)
        fit_scores.append(
            {
                "role": role_name,
                "score": round((matched_weight / total_weight) * 100) if total_weight else 0,
                "matched_skills": [skill for skill, _ in top_skills if skill in profile_skills][:4],
                "missing_skills": [skill for skill, _ in top_skills if skill not in profile_skills][:4],
            }
        )
    fit_scores.sort(key=lambda row: row["score"], reverse=True)
    return fit_scores


def compute_skill_gap(
    connection: sqlite3.Connection,
    profile_skills: set[str],
    target_roles: list[str],
) -> dict[str, object]:
    cursor = connection.cursor()
    if target_roles:
        placeholders = ", ".join("?" for _ in target_roles)
        cursor.execute(
            f"""
        SELECT skill, COUNT(DISTINCT job_id) AS openings
        FROM job_skills
        WHERE role_name IN ({placeholders})
        GROUP BY skill
        ORDER BY openings DESC, skill ASC
        """,
            target_roles,
        )
        total_jobs = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM job_postings
            WHERE role_name IN ({placeholders})
            """,
            target_roles,
        ).fetchone()[0]
    else:
        cursor.execute(
            """
        SELECT skill, COUNT(DISTINCT job_id) AS openings
        FROM job_skills
        GROUP BY skill
        ORDER BY openings DESC, skill ASC
        """
        )
        total_jobs = connection.execute("SELECT COUNT(*) FROM job_postings").fetchone()[0]
    rows = cursor.fetchall()

    strengths = []
    gaps = []
    for skill, openings in rows:
        item = {
            "skill": skill,
            "openings": openings,
            "demand_pct": round((openings / total_jobs) * 100, 1),
        }
        if skill in profile_skills:
            strengths.append(item)
        else:
            gaps.append(item)

    coverage_numerator = sum(item["openings"] for item in strengths[:10])
    coverage_denominator = sum(openings for _, openings in rows[:10])
    return {
        "market_coverage": round((coverage_numerator / coverage_denominator) * 100) if coverage_denominator else 0,
        "priority_gaps": gaps[:6],
        "existing_strengths": strengths[:6],
    }


def build_roadmap(priority_gaps: list[dict[str, object]], best_role: str) -> list[dict[str, object]]:
    skills = [item["skill"] for item in priority_gaps]
    return [
        {
            "phase": "Month 1",
            "focus": ", ".join(skills[:2]) if skills[:2] else "Power BI foundations",
            "outcome": "Build two recruiter-friendly mini dashboards and explain the KPI logic behind every chart.",
        },
        {
            "phase": "Month 2",
            "focus": ", ".join(skills[2:4]) if skills[2:4] else "Dashboarding and communication",
            "outcome": f"Turn the strongest-fit path into a complete {best_role} case study with measurable recommendations.",
        },
        {
            "phase": "Month 3",
            "focus": ", ".join(skills[4:6]) if skills[4:6] else "Advanced BI polish",
            "outcome": "Add SQL snippets, assumptions, and stakeholder-facing insight summaries for interview storytelling.",
        },
    ]


def top_role_city_skills(connection: sqlite3.Connection) -> list[dict[str, object]]:
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT role_name, city, skill, COUNT(*) AS demand
        FROM job_skills
        GROUP BY role_name, city, skill
        """
    )

    grouped: dict[tuple[str, str], list[tuple[str, int]]] = defaultdict(list)
    for role_name, city, skill, demand in cursor.fetchall():
        grouped[(role_name, city)].append((skill, demand))

    highlights = []
    for (role_name, city), rows in grouped.items():
        rows.sort(key=lambda row: row[1], reverse=True)
        highlights.append(
            {
                "role": role_name,
                "city": city,
                "top_skill": rows[0][0],
                "top_skill_demand": rows[0][1],
            }
        )
    highlights.sort(key=lambda row: row["top_skill_demand"], reverse=True)
    return highlights[:8]


def build_insights(
    connection: sqlite3.Connection,
    target_role_fit: list[dict[str, object]],
    skill_gap: dict[str, object],
) -> list[str]:
    total_jobs = connection.execute("SELECT COUNT(*) FROM job_postings").fetchone()[0]
    top_skill = connection.execute(
        """
        SELECT skill, COUNT(DISTINCT job_id) AS openings
        FROM job_skills
        GROUP BY skill
        ORDER BY openings DESC, skill ASC
        LIMIT 1
        """
    ).fetchone()
    ncr_jobs = connection.execute(
        """
        SELECT COUNT(*)
        FROM job_postings
        WHERE city IN ('New Delhi', 'Gurugram', 'Noida')
        """
    ).fetchone()[0]
    ncr_share = round((ncr_jobs / total_jobs) * 100)
    best_fit = target_role_fit[0]
    top_gap = skill_gap["priority_gaps"][0]
    return [
        f"{top_skill[0]} appears in {round((top_skill[1] / total_jobs) * 100)}% of openings, making it the clearest baseline skill in the market sample.",
        f"Delhi NCR accounts for {ncr_share}% of openings in this dataset, making it the strongest early-career region to target first.",
        f"Your strongest fit today is {best_fit['role']} at {best_fit['score']}% alignment, while {top_gap['skill']} is the highest-value gap to close next.",
    ]


def build_analysis(connection: sqlite3.Connection, profile: dict[str, object], rows: list[dict[str, object]]) -> dict[str, object]:
    profile_skills = set(profile["normalized_skills"])
    role_fit = compute_role_fit(connection, profile_skills)
    target_role_fit = [item for item in role_fit if item["role"] in profile["target_roles"]] or role_fit
    skill_gap = compute_skill_gap(connection, profile_skills, profile["target_roles"])

    analysis = {
        "meta": {
            "project_name": "HireLens",
            "subtitle": "Job Market Skill Gap Analyzer",
            "generated_on": TODAY.isoformat(),
            "candidate_name": profile["candidate_name"],
        },
        "summary": {
            "total_jobs": connection.execute("SELECT COUNT(*) FROM job_postings").fetchone()[0],
            "total_companies": connection.execute("SELECT COUNT(DISTINCT company) FROM job_postings").fetchone()[0],
            "average_salary_lpa": round(connection.execute("SELECT AVG(salary_lpa) FROM job_postings").fetchone()[0], 1),
            "best_fit_role": target_role_fit[0]["role"],
            "market_coverage": skill_gap["market_coverage"],
        },
        "profile": {
            "target_roles": profile["target_roles"],
            "current_skills": profile["normalized_skills"],
            "learning_goal": profile["learning_goal"],
        },
        "charts": {
            "role_distribution": query_pairs(
                connection,
                """
                SELECT role_name, COUNT(*)
                FROM job_postings
                GROUP BY role_name
                ORDER BY COUNT(*) DESC
                """,
                8,
            ),
            "city_distribution": query_pairs(
                connection,
                """
                SELECT city, COUNT(*)
                FROM job_postings
                GROUP BY city
                ORDER BY COUNT(*) DESC
                """,
                8,
            ),
            "work_mode_distribution": query_pairs(
                connection,
                """
                SELECT work_mode, COUNT(*)
                FROM job_postings
                GROUP BY work_mode
                ORDER BY COUNT(*) DESC
                """,
                4,
            ),
            "top_skills": query_pairs(
                connection,
                """
                SELECT skill, COUNT(DISTINCT job_id)
                FROM job_skills
                GROUP BY skill
                ORDER BY COUNT(DISTINCT job_id) DESC, skill ASC
                """,
                12,
            ),
        },
        "role_fit": target_role_fit,
        "skill_gap": skill_gap,
        "city_role_highlights": top_role_city_skills(connection),
        "roadmap": build_roadmap(skill_gap["priority_gaps"], target_role_fit[0]["role"]),
        "insights": build_insights(connection, target_role_fit, skill_gap),
        "sample_jobs": [
            {
                "job_id": row["job_id"],
                "title": row["title"],
                "company": row["company"],
                "city": row["city"],
                "experience_level": row["experience_level"],
                "salary_lpa": row["salary_lpa"],
                "skills": row["skills"].split("|")[:4],
            }
            for row in rows[:10]
        ],
    }
    return analysis


def write_outputs(analysis: dict[str, object]) -> None:
    with ANALYSIS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(analysis, handle, indent=2)
    with DASHBOARD_DATA_PATH.open("w", encoding="utf-8") as handle:
        handle.write("window.ANALYSIS_DATA = " + json.dumps(analysis, indent=2) + ";")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    rows = generate_job_rows()
    write_csv(rows)
    profile = load_profile()
    connection = build_database(rows)
    try:
        analysis = build_analysis(connection, profile, rows)
    finally:
        connection.close()
    write_outputs(analysis)

    print(f"Generated {CSV_PATH}")
    print(f"Generated {DB_PATH}")
    print(f"Generated {ANALYSIS_PATH}")
    print(f"Generated {DASHBOARD_DATA_PATH}")


if __name__ == "__main__":
    main()
