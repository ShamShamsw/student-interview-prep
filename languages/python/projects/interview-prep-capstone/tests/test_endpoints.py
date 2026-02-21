from fastapi.testclient import TestClient

import final.app as api

client = TestClient(api.app)


def setup_function() -> None:
    api.ATTEMPTS.clear()
    api.STUDY_PLANS.clear()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_attempt_and_progress() -> None:
    payload = {
        "user_id": 1,
        "problem_id": "01-two-sum",
        "topic": "arrays",
        "difficulty": "easy",
        "solved": True,
        "minutes_spent": 20,
    }
    response = client.post("/attempts", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 1

    progress = client.get("/progress/1")
    assert progress.status_code == 200
    assert progress.json() == {
        "user_id": 1,
        "total_attempts": 1,
        "solved_attempts": 1,
        "solve_rate": 1.0,
    }


def test_recommendations_prioritize_weaker_topic() -> None:
    events = [
        {
            "user_id": 1,
            "problem_id": "01-two-sum",
            "topic": "arrays",
            "difficulty": "easy",
            "solved": True,
            "minutes_spent": 15,
        },
        {
            "user_id": 1,
            "problem_id": "08-group-anagrams",
            "topic": "arrays",
            "difficulty": "medium",
            "solved": True,
            "minutes_spent": 25,
        },
        {
            "user_id": 1,
            "problem_id": "32-number-of-islands",
            "topic": "graphs",
            "difficulty": "medium",
            "solved": False,
            "minutes_spent": 35,
        },
    ]

    for event in events:
        response = client.post("/attempts", json=event)
        assert response.status_code == 200

    response = client.get("/recommendations/1")
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == 1
    assert body["recommended_topics"][0] == "graphs"


def test_recommendations_empty_for_user_without_attempts() -> None:
    response = client.get("/recommendations/999")
    assert response.status_code == 200
    assert response.json() == {"user_id": 999, "recommended_topics": []}


def test_upsert_study_plan() -> None:
    response = client.post(
        "/study-plan/1",
        json={"focus_topics": ["graphs", "dp"], "sessions_per_week": 4},
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "focus_topics": ["graphs", "dp"],
        "sessions_per_week": 4,
    }


def test_attempt_validation_error_for_minutes() -> None:
    response = client.post(
        "/attempts",
        json={
            "user_id": 1,
            "problem_id": "01-two-sum",
            "topic": "arrays",
            "difficulty": "easy",
            "solved": True,
            "minutes_spent": 0,
        },
    )
    assert response.status_code == 422


def test_study_plan_validation_error_for_empty_topics() -> None:
    response = client.post(
        "/study-plan/1",
        json={"focus_topics": [], "sessions_per_week": 3},
    )
    assert response.status_code == 422
