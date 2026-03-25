SELECT role_name, COUNT(*) AS openings
FROM job_postings
GROUP BY role_name
ORDER BY openings DESC;

SELECT city, COUNT(*) AS openings
FROM job_postings
GROUP BY city
ORDER BY openings DESC;

SELECT skill, COUNT(DISTINCT job_id) AS openings
FROM job_skills
GROUP BY skill
ORDER BY openings DESC, skill ASC
LIMIT 12;

SELECT role_name, skill, COUNT(*) AS demand
FROM job_skills
GROUP BY role_name, skill
ORDER BY role_name ASC, demand DESC;

SELECT city, role_name, COUNT(*) AS openings, ROUND(AVG(salary_lpa), 1) AS avg_salary_lpa
FROM job_postings
GROUP BY city, role_name
ORDER BY openings DESC;
