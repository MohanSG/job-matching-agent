import re

def remove_duplicates(jobs):
    deduped_jobs = {}
    for job in jobs:
        if job["jobId"] not in deduped_jobs:
            deduped_jobs[job["jobId"]] = job
    return list(deduped_jobs.values())

def build_pattern(words):
    if not words:
        return None
    
    joined = "|".join(re.escape(w) for w in words)
    return re.compile(rf"\b({joined})\b", re.IGNORECASE)
    
def filter_jobs(jobs, excluded_titles, excluded_companies):
    title_re = build_pattern(excluded_titles)
    company_re = build_pattern(excluded_companies)

    filtered_jobs = []
    for job in jobs:
        title_hit = title_re and title_re.search(job["jobTitle"])
        company_hit = company_re and company_re.search(job["employerName"])

        if title_hit or company_hit:
            matched = (title_hit or company_hit).group()
            print(f"Dropping {job["employerName"]} - {job["jobTitle"]}, matched: {matched}")
            continue

        print(f"Appending {job["employerName"]} - {job["jobTitle"]}")
        filtered_jobs.append(job)
    return filtered_jobs