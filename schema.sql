CREATE TABLE IF NOT EXISTS jobs (
    id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source         TEXT NOT NULL,
    job_id         TEXT NOT NULL,
    title          TEXT NOT NULL,
    company        TEXT,
    location       TEXT,
    salary_min     NUMERIC,
    salary_max     NUMERIC,
    url            TEXT NOT NULL,
    description    TEXT,
    posted_at      TIMESTAMPTZ,
    expires_at     TIMESTAMPTZ,
    first_seen_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    score          SMALLINT CHECK (score BETWEEN 0 AND 100),
    reasons        TEXT[],
    red_flags      TEXT[],
    missing_skills TEXT[],
    scored_at      TIMESTAMPTZ,
    model          TEXT,

    notified       BOOLEAN NOT NULL DEFAULT FALSE,
    status         TEXT NOT NULL DEFAULT 'new',

    UNIQUE (source, job_id)
);

CREATE INDEX IF NOT EXISTS jobs_score_idx
    ON jobs (score DESC);

CREATE INDEX IF NOT EXISTS jobs_unnotified_idx
    ON jobs (score DESC) WHERE NOT notified;