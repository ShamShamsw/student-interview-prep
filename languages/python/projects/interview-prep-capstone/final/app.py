"""Final: Interview Prep Platform Capstone API.

Run:
  uvicorn app:app --reload
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Interview Prep Platform Capstone (Final)")


class AttemptIn(BaseModel):
    user_id: int
    problem_id: str
    topic: str
    difficulty: str
    solved: bool
    minutes_spent: int = Field(gt=0)


class AttemptOut(AttemptIn):
    id: int


class ProgressOut(BaseModel):
    user_id: int
    total_attempts: int
    solved_attempts: int
    solve_rate: float


class RecommendationOut(BaseModel):
    user_id: int
    recommended_topics: List[str]


class StudyPlanIn(BaseModel):
    focus_topics: List[str] = Field(min_length=1)
    sessions_per_week: int = Field(gt=0)


class StudyPlanOut(StudyPlanIn):
    user_id: int


@dataclass
class AttemptRecord:
    id: int
    user_id: int
    problem_id: str
    topic: str
    difficulty: str
    solved: bool
    minutes_spent: int


ATTEMPTS: List[AttemptRecord] = []
STUDY_PLANS: dict[int, StudyPlanOut] = {}


def create_attempt(payload: AttemptIn) -> AttemptOut:
    record = AttemptRecord(id=len(ATTEMPTS) + 1, **payload.model_dump())
    ATTEMPTS.append(record)
    return AttemptOut(**record.__dict__)


def build_progress(user_id: int) -> ProgressOut:
    user_attempts = [attempt for attempt in ATTEMPTS if attempt.user_id == user_id]
    total = len(user_attempts)
    solved = sum(1 for attempt in user_attempts if attempt.solved)
    rate = round((solved / total), 3) if total else 0.0
    return ProgressOut(
        user_id=user_id,
        total_attempts=total,
        solved_attempts=solved,
        solve_rate=rate,
    )


def recommend_topics(user_id: int, top_k: int = 3) -> RecommendationOut:
    user_attempts = [attempt for attempt in ATTEMPTS if attempt.user_id == user_id]
    if not user_attempts:
        return RecommendationOut(user_id=user_id, recommended_topics=[])

    topic_stats: dict[str, list[bool]] = defaultdict(list)
    for attempt in user_attempts:
        topic_stats[attempt.topic].append(attempt.solved)

    ranking = []
    for topic, outcomes in topic_stats.items():
        solved_ratio = sum(1 for outcome in outcomes if outcome) / len(outcomes)
        ranking.append((solved_ratio, -len(outcomes), topic))

    ranking.sort()
    topics = [topic for _, _, topic in ranking[:top_k]]
    return RecommendationOut(user_id=user_id, recommended_topics=topics)


def upsert_study_plan(user_id: int, payload: StudyPlanIn) -> StudyPlanOut:
    plan = StudyPlanOut(user_id=user_id, **payload.model_dump())
    STUDY_PLANS[user_id] = plan
    return plan


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/attempts", response_model=AttemptOut)
def api_create_attempt(payload: AttemptIn) -> AttemptOut:
    return create_attempt(payload)


@app.get("/progress/{user_id}", response_model=ProgressOut)
def api_get_progress(user_id: int) -> ProgressOut:
    return build_progress(user_id)


@app.get("/recommendations/{user_id}", response_model=RecommendationOut)
def api_get_recommendations(user_id: int) -> RecommendationOut:
    return recommend_topics(user_id)


@app.post("/study-plan/{user_id}", response_model=StudyPlanOut)
def api_upsert_study_plan(user_id: int, payload: StudyPlanIn) -> StudyPlanOut:
    if not payload.focus_topics:
        raise HTTPException(status_code=400, detail="focus_topics cannot be empty")
    return upsert_study_plan(user_id, payload)
