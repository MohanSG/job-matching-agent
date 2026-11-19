from openai import OpenAI
import os
import json

client = OpenAI()
PROMPT = """
        You role is to screen jobs for a candidation with a specific profile, You will give the job a score between 0 and 100.
        80+ is a strong score, 50-79 is good and anything below 50 is poor. You need to read through the profile and pay attention to the
        profiles wants and dealbrekers. If there is a dealbreaker it should greatly affect the score in a negative way, if the jobs has a want,
        it should increase the score of the job. Only base your judgement on the text that is given. ASsume salarys are in GBP

        The output should be given in a JSON format, There should be 4 fields, score (integer - 0 - 100), reason (string - 3 lines stating justifying the score),
        red_flags(list), and missing_skills(list). Also include the company name, job name, id, description, min and max salary, date posted and applications.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "score": {
            "type": "integer",
            "description": "Fit score from 0 to 100. 80+ strong fit, 50-79 possible, under 50 poor fit. Any dealbreaker means under 30.",
        },
        "reasons": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Exactly 3 short reasons for the score, based only on the job text.",
        },
        "red_flags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Dealbreakers or concerns found in the advert. Empty list if none.",
        },
        "missing_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Skills or experience the job asks for that the candidate lacks. Empty list if none.",
        },
    },
    "required": ["score", "reasons", "red_flags", "missing_skills"],
    "additionalProperties": False,
}


def build_user_message(job, profile):
    wants = "\n".join(f"- {w}" for w in profile["wants"])
    dealbreakers = "\n".join(f"- {d}" for d in profile["dealbreakers"])
    skills = "\n".join(f"- {s}" for s in profile["skills"])

    return f"""
            CANDIDATE PROFILE:
            Summary: {profile["summary"]}
            Wants: {wants}
            Dealbreakers: {dealbreakers}
            Skills: {skills}

            JOB:
            Employer: {job["employerName"]}
            Job Title: {job["jobTitle"]}
            Job Description: {job["jobDescription"]}
            Minimum Salary: {job["minimumSalary"] or "not listed"}
            Maximum Salary: {job["maximumSalary"] or "not listed"}
"""


def score_jobs(jobs, profile):
    for job in jobs:
        response = client.responses.create(
            model=os.environ["SCORE_MODEL"],
            instructions=PROMPT,
            input=build_user_message(job, profile),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "job_score",
                    "strict": True,
                    "schema": SCHEMA,
                }
            },
        )
        result = json.loads(response.output_text)
        result['job'] = {'name' : job["jobTitle"],
                        'company' : job["employerName"]}
        print(result)
