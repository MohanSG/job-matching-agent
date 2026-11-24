import psycopg
import os
from pathlib import Path
from datetime import datetime


def get_db():
    return psycopg.connect(os.environ["DATABASE_URL"])


def check_db():
    SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.sql"

    with get_db() as conn:
        conn.execute(SCHEMA_PATH.read_text())


def existing_job_ids(job_ids, source):
    with get_db() as conn:
        rows = conn.execute(
            """
        SELECT job_id from jobs WHERE source=%s AND job_id=ANY(%s)    
        """,
            (source, job_ids),
        ).fetchall()
        return {row[0] for row in rows}


def insert_job(job, job_score, source):
    row = {
        "source": source,
        "jobId": str(job["jobId"]),
        "title": job["jobTitle"],
        "company": job["employerName"],
        "location": job["locationName"],
        "salary_min": job.get("minimumSalary"),
        "salary_max": job.get("maximumSalary"),
        "url": job["jobUrl"],
        "description": job["jobDescription"],
        "posted_at": datetime.strptime(job["date"], "%d/%m/%Y"),
        "expires_at": datetime.strptime(job["expirationDate"], "%d/%m/%Y"),
        "score": job_score["score"],
        "reasons": job_score["reasons"],
        "red_flags": job_score["red_flags"],
        "missing_skills": job_score["missing_skills"],
        "model": os.environ["SCORE_MODEL"],
    }
    with get_db() as conn:
        conn.execute(
            """
        INSERT INTO jobs (source, job_id, title, company, location, salary_min, salary_max, url, description, posted_at,
          expires_at, score, reasons, red_flags, missing_skills, scored_at, model)
        VALUES (%(source)s, %(jobId)s, %(title)s, %(company)s, %(location)s, %(salary_min)s, %(salary_max)s, %(url)s, %(description)s, 
                %(posted_at)s, %(expires_at)s, %(score)s, %(reasons)s, %(red_flags)s, %(missing_skills)s, now(), %(model)s)
        ON CONFLICT (source, job_id) DO NOTHING
        """,
            row,
        )
