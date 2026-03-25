const data = window.ANALYSIS_DATA;

function numberFormat(value) {
  return new Intl.NumberFormat("en-IN").format(value);
}

function renderSummary() {
  const cards = [
    {
      label: "Openings",
      value: numberFormat(data.summary.total_jobs),
      note: "Synthetic postings in the local dataset",
    },
    {
      label: "Companies",
      value: numberFormat(data.summary.total_companies),
      note: "Distinct employers represented",
    },
    {
      label: "Average Salary",
      value: `${data.summary.average_salary_lpa} LPA`,
      note: "Across all roles and experience bands",
    },
    {
      label: "Best Fit",
      value: data.summary.best_fit_role,
      note: `${data.summary.market_coverage}% top-skill coverage with the current profile`,
    },
  ];

  document.getElementById("summary-cards").innerHTML = cards
    .map(
      (card) => `
        <article class="summary-card">
          <span>${card.label}</span>
          <strong>${card.value}</strong>
          <span>${card.note}</span>
        </article>
      `
    )
    .join("");

  document.getElementById("hero-text").textContent =
    `${data.profile.learning_goal} Generated on ${data.meta.generated_on} for ${data.meta.candidate_name}, combining Python, SQLite, and dashboard storytelling into a single recruiter-friendly case study.`;
}

function renderInsights() {
  document.getElementById("insight-list").innerHTML = data.insights
    .map(
      (item) => `
        <article class="insight-item">
          <p>${item}</p>
        </article>
      `
    )
    .join("");
}

function renderTopSkills() {
  const topValue = data.charts.top_skills[0]?.value || 1;
  document.getElementById("skill-bars").innerHTML = data.charts.top_skills
    .map((item) => {
      const width = Math.max(8, Math.round((item.value / topValue) * 100));
      return `
        <div class="bar-row">
          <strong>${item.label}</strong>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${width}%"></div>
          </div>
          <span>${item.value}</span>
        </div>
      `;
    })
    .join("");
}

function renderRoleFit() {
  document.getElementById("role-fit-list").innerHTML = data.role_fit
    .map(
      (item) => `
        <article class="fit-card">
          <header>
            <h3>${item.role}</h3>
            <span class="score-pill">${item.score}%</span>
          </header>
          <small>Matched skills</small>
          <div class="tag-row">
            ${item.matched_skills.map((skill) => `<span class="tag">${skill}</span>`).join("")}
          </div>
          <small>Missing next-step skills</small>
          <div class="tag-row">
            ${item.missing_skills.map((skill) => `<span class="chip">${skill}</span>`).join("")}
          </div>
        </article>
      `
    )
    .join("");
}

function renderGaps() {
  document.getElementById("gap-list").innerHTML = data.skill_gap.priority_gaps
    .map(
      (item) => `
        <div class="gap-item">
          <div>
            <strong>${item.skill}</strong>
            <span>Appears in ${item.demand_pct}% of sampled openings</span>
          </div>
          <span class="score-pill">${item.openings}</span>
        </div>
      `
    )
    .join("");
}

function renderCities() {
  document.getElementById("city-cards").innerHTML = data.city_role_highlights
    .map(
      (item) => `
        <article class="mini-card">
          <header>
            <h3>${item.city}</h3>
            <span class="chip">${item.role}</span>
          </header>
          <strong>${item.top_skill}</strong>
          <p>Strongest recurring skill in this role-city cluster across the local market sample.</p>
        </article>
      `
    )
    .join("");
}

function renderRoadmap() {
  document.getElementById("roadmap").innerHTML = data.roadmap
    .map(
      (item) => `
        <article class="roadmap-card">
          <header>
            <h3>${item.phase}</h3>
            <span class="score-pill">${item.focus}</span>
          </header>
          <p>${item.outcome}</p>
        </article>
      `
    )
    .join("");
}

function renderJobs() {
  document.getElementById("job-table").innerHTML = data.sample_jobs
    .map(
      (item) => `
        <tr>
          <td>${item.title}</td>
          <td>${item.company}</td>
          <td>${item.city}</td>
          <td>${item.experience_level}</td>
          <td>${item.salary_lpa} LPA</td>
          <td>
            <div class="skill-stack">
              ${item.skills.map((skill) => `<span class="tag">${skill}</span>`).join("")}
            </div>
          </td>
        </tr>
      `
    )
    .join("");
}

renderSummary();
renderInsights();
renderTopSkills();
renderRoleFit();
renderGaps();
renderCities();
renderRoadmap();
renderJobs();
