"""Final: Interview Patterns API.

Run:
  uvicorn app:app --reload
"""

from __future__ import annotations

from collections import Counter
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Interview Patterns API (Final)")


class TwoSumRequest(BaseModel):
    nums: List[int] = Field(min_length=2)
    target: int


class TwoSumResponse(BaseModel):
    indices: List[int]


class ParenthesesRequest(BaseModel):
    s: str


class ParenthesesResponse(BaseModel):
    valid: bool


class TopKRequest(BaseModel):
    nums: List[int] = Field(min_length=1)
    k: int = Field(gt=0)


class TopKResponse(BaseModel):
    values: List[int]


class PracticeEvent(BaseModel):
    topic: str
    minutes: int = Field(gt=0)
    difficulty: str


class PracticeEventOut(PracticeEvent):
    id: int


class TopTopicsResponse(BaseModel):
    topics: List[str]


class MinutesPairResponse(BaseModel):
    indices: List[int]


EVENTS: List[PracticeEventOut] = []


def two_sum_indices(nums: List[int], target: int) -> List[int]:
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        needed = target - value
        if needed in seen:
            return [seen[needed], index]
        seen[value] = index
    return []


def is_valid_parentheses(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for char in s:
        if char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
        else:
            stack.append(char)

    return len(stack) == 0


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    counts = Counter(nums)
    return [value for value, _ in counts.most_common(k)]


def top_practiced_topics(k: int) -> List[str]:
    counts = Counter(event.topic for event in EVENTS)
    return [topic for topic, _ in counts.most_common(k)]


def find_minutes_pair(target: int) -> List[int]:
    minutes = [event.minutes for event in EVENTS]
    return two_sum_indices(minutes, target)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/algorithms/two-sum", response_model=TwoSumResponse)
def api_two_sum(payload: TwoSumRequest) -> TwoSumResponse:
    indices = two_sum_indices(payload.nums, payload.target)
    if not indices:
        raise HTTPException(status_code=404, detail="No valid pair found")
    return TwoSumResponse(indices=indices)


@app.post("/algorithms/valid-parentheses", response_model=ParenthesesResponse)
def api_valid_parentheses(payload: ParenthesesRequest) -> ParenthesesResponse:
    return ParenthesesResponse(valid=is_valid_parentheses(payload.s))


@app.post("/algorithms/top-k-frequent", response_model=TopKResponse)
def api_top_k(payload: TopKRequest) -> TopKResponse:
    if payload.k > len(payload.nums):
        raise HTTPException(status_code=400, detail="k cannot exceed number of items")
    return TopKResponse(values=top_k_frequent(payload.nums, payload.k))


@app.post("/practice/events", response_model=PracticeEventOut)
def add_practice_event(payload: PracticeEvent) -> PracticeEventOut:
    event = PracticeEventOut(id=len(EVENTS) + 1, **payload.model_dump())
    EVENTS.append(event)
    return event


@app.get("/practice/events", response_model=List[PracticeEventOut])
def list_practice_events() -> List[PracticeEventOut]:
    return EVENTS


@app.get("/practice/insights/top-topics", response_model=TopTopicsResponse)
def api_top_topics(k: int = 3) -> TopTopicsResponse:
    if k <= 0:
        raise HTTPException(status_code=400, detail="k must be positive")
    return TopTopicsResponse(topics=top_practiced_topics(k))


@app.get("/practice/insights/minutes-pair", response_model=MinutesPairResponse)
def api_minutes_pair(target: int) -> MinutesPairResponse:
    if target <= 0:
        raise HTTPException(status_code=400, detail="target must be positive")
    indices = find_minutes_pair(target)
    if not indices:
        raise HTTPException(status_code=404, detail="No matching pair found")
    return MinutesPairResponse(indices=indices)
