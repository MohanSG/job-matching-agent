import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_jobs(title, location, radius, resultsToTake):
    job_search_url = "https://www.reed.co.uk/api/1.0/search"
    params = {
        "keywords": title,
        "locationName": location,
        "distanceFromLocation": radius,
        "resultsToTake": resultsToTake,
    }

    response = requests.get(
        job_search_url, params, auth=(os.environ["REED_API_KEY"], ""), timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return data["results"]

def get_job_details(session, job_id):
    job_details_url = "https://www.reed.co.uk/api/1.0/jobs/"

    response = session.get(
        f"{job_details_url}{job_id}",auth=(os.environ["REED_API_KEY"], ""), timeout=30
    )
    data = response.json()
    return data

def add_full_descriptions(jobs):
    with requests.Session() as session:
        session.auth = (os.environ["REED_API_KEY"], "")

        detailed_jobs = []
        for job in jobs:
            detail = get_job_details(session, job["jobId"])
            job["jobDescription"] = detail["jobDescription"]
            detailed_jobs.append(job)

        return detailed_jobs
    