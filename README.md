# Job Matching Agent

A Python tool that pulls junior developer jobs from the Reed API and scores each one against my profile with the OpenAI API, so I only read the ones worth applying for.

## Why I built it

I'm looking for a junior developer role in London. A lot of time goes on opening adverts that turn out to want 3+ years of experience or security clearance. This does that first pass for me.

## How it works

1. **Search:** runs a Reed search for every job title in `profile.yaml`, within a set radius of a location.
2. **Remove duplicates:** the same advert often comes back for several titles, so jobs are deduplicated by Reed job ID.
3. **Filter:** drops jobs whose title or company matches an excluded word (senior, lead, manager and so on). It matches whole words only, so `intern` doesn't knock out "Internal Tools Developer".
4. **Get full descriptions:** search results only include a short snippet, so it calls Reed's job details endpoint for each job that's left.
5. **Score:** sends the job and my profile to the OpenAI Responses API. It uses structured outputs with a strict JSON schema, so every response comes back in the same shape:

```json
{
  "score": 72,
  "reasons": ["...", "...", "..."],
  "red_flags": [],
  "missing_skills": ["TypeScript"]
}
```

A score of 80+ is a strong fit, 50 to 79 is possible, and under 50 is poor. Any dealbreaker in the advert pushes the score under 30.

## Setup

You need Python 3.12 or newer, because the code uses f-strings with nested quotes.

```bash
git clone https://github.com/MohanSG/job-matching-agent.git
cd job-matching-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
REED_API_KEY=your-reed-api-key
OPENAI_API_KEY=your-openai-api-key
SCORE_MODEL=your-model-name
```

- Get a free Reed API key at [reed.co.uk/developers](https://www.reed.co.uk/developers).
- `SCORE_MODEL` can be any OpenAI model that supports structured outputs.

## Configure

Everything about the search and the candidate lives in `profile.yaml`:

- `search`: job titles, location, radius in miles and results per title
- `filters`: words in job titles and company names to skip
- `profile`: summary, skills, wants and dealbreakers, which the model uses to score each job

## Run

From the project root:

```bash
python -m jobagent
```

Run it from the root folder, because it reads `profile.yaml` from the current directory.

## Built with

Python, Requests, OpenAI Responses API (structured outputs), PyYAML, python-dotenv

## Next steps

- Score every filtered job and print a ranked shortlist
- Add Adzuna as a second job source
- Save jobs and scores to PostgreSQL
- Send a daily email digest of the best matches
