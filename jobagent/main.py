from jobagent.sources import get_jobs, add_full_descriptions
from jobagent.config import parse_yaml
from jobagent.utils import remove_duplicates, filter_jobs
from jobagent.scorer import score_jobs
from jobagent.db import existing_job_ids, check_db

def main():
    profile = parse_yaml() #Parse profile details and filters from profile.yaml

    #Checks filtering options and job requirements in profile.yaml
    results_to_take = profile["search"]["results_per_title"]
    titles = profile["search"]["titles"]
    location = profile["search"]["location"]
    radius = profile["search"]["radius_miles"]

    exclude_titles = profile["filters"]["exclude_title_words"]
    exclude_companies = profile["filters"]["exclude_companies"]

    #Gets jobs from REED API and stores them into all_jobs
    all_jobs = []
    for title in titles:
        jobs = get_jobs(title, location, radius, results_to_take)
        all_jobs.extend(jobs)

    #Removes duplcations and filters job based on filters set in profile.yaml
    deduped_jobs = remove_duplicates(all_jobs)
    filtered_jobs = filter_jobs(deduped_jobs, exclude_titles, exclude_companies)

    #Initializes DB if it hasnt already and gets all jobs stored from previous job search.
    #Then removes any jobs already scored
    check_db()
    known = existing_job_ids([str(j["jobId"]) for j in filtered_jobs], "reed")
    new_jobs = [j for j in filtered_jobs if(str(j["jobId"])) not in known]

    #Filtering details with job count
    print(f"All jobs count - {len(all_jobs)}")
    print(f"Job count after duplicates deleted - {len(deduped_jobs)}")
    print(f"Job count after filtering - {len(filtered_jobs)}")
    print(f"Job count after checking existing jobs - {len(new_jobs)}")

    #Grabs full job descriptions for each job and replaces the shorter job descriptions.
    detailed_jobs = add_full_descriptions(new_jobs)

    #API call to OpenAI API to score jobs and insert them into the jobs table. Check schema.sql for jobs table schema
    score_jobs(detailed_jobs, profile["profile"], "reed")

if __name__ == "__main__":
    main()
    