"""Starter: Interview Prep Platform Capstone API.

Run:
  uvicorn app:app --reload
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Interview Prep Platform Capstone (Starter)")


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
    """Create and store a new attempt.

    TODO:
    - Create AttemptRecord with incremental id.
    - Store it in ATTEMPTS.
    - Return AttemptOut.
    """
    raise NotImplementedError("Implement create_attempt")


def build_progress(user_id: int) -> ProgressOut:
    """Compute progress metrics for a user.

    TODO:
    - Filter ATTEMPTS for user_id.
    - Compute total_attempts, solved_attempts, solve_rate.
    - Return ProgressOut.
    """
    raise NotImplementedError("Implement build_progress")


def recommend_topics(user_id: int, top_k: int = 3) -> RecommendationOut:
    """Recommend topics based on weak solved ratio.

    TODO:
    - Group attempts by topic for user.
    - Rank by lowest solve ratio first (weakest topics).
    - Return up to top_k topics.
    """
    raise NotImplementedError("Implement recommend_topics")


def upsert_study_plan(user_id: int, payload: StudyPlanIn) -> StudyPlanOut:
    """Create or update a study plan for user.

    TODO:
    - Save StudyPlanOut in STUDY_PLANS.
    - Return saved plan.
    """
    raise NotImplementedError("Implement upsert_study_plan")


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
