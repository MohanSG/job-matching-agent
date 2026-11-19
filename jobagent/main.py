from jobagent.sources import get_jobs, add_full_descriptions
from jobagent.config import parse_yaml
from jobagent.utils import remove_duplicates, filter_jobs
from jobagent.scorer import score_jobs

def main():
    profile = parse_yaml()

    results_to_take = profile["search"]["results_per_title"]
    titles = profile["search"]["titles"]
    location = profile["search"]["location"]
    radius = profile["search"]["radius_miles"]
    
    exclude_titles = profile["filters"]["exclude_title_words"]
    exclude_companies = profile["filters"]["exclude_companies"]

    all_jobs = []
    for title in titles:
        jobs = get_jobs(title, location, radius, results_to_take)
        all_jobs.extend(jobs)

    deduped_jobs = remove_duplicates(all_jobs)
    filtered_jobs = filter_jobs(deduped_jobs, exclude_titles, exclude_companies)

    print(f"All jobs count - {len(all_jobs)}")
    print(f"Job count after duplicates deleted - {len(deduped_jobs)}")
    print(f"Job count after filtering - {len(filtered_jobs)}")

    detailed_jobs = add_full_descriptions(filtered_jobs)

    score_jobs(detailed_jobs, profile["profile"])

if __name__ == "__main__":
    main()
    