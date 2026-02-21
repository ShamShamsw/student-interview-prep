from fastapi.testclient import TestClient

import final.app as api

client = TestClient(api.app)


def setup_function() -> None:
    api.EVENTS.clear()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_two_sum_success() -> None:
    response = client.post(
        "/algorithms/two-sum",
        json={"nums": [2, 7, 11, 15], "target": 9},
    )
    assert response.status_code == 200
    assert response.json() == {"indices": [0, 1]}


def test_two_sum_not_found() -> None:
    response = client.post(
        "/algorithms/two-sum",
        json={"nums": [1, 2, 3], "target": 999},
    )
    assert response.status_code == 404


def test_valid_parentheses() -> None:
    response = client.post("/algorithms/valid-parentheses", json={"s": "()[]{}"})
    assert response.status_code == 200
    assert response.json() == {"valid": True}


def test_top_k_frequent_success() -> None:
    response = client.post(
        "/algorithms/top-k-frequent",
        json={"nums": [1, 1, 1, 2, 2, 3], "k": 2},
    )
    assert response.status_code == 200
    assert response.json() == {"values": [1, 2]}


def test_top_k_frequent_bad_request() -> None:
    response = client.post(
        "/algorithms/top-k-frequent",
        json={"nums": [1, 2], "k": 3},
    )
    assert response.status_code == 400


def test_practice_events_and_top_topics() -> None:
    payloads = [
        {"topic": "arrays", "minutes": 45, "difficulty": "easy"},
        {"topic": "arrays", "minutes": 30, "difficulty": "medium"},
        {"topic": "graphs", "minutes": 30, "difficulty": "medium"},
    ]

    for payload in payloads:
        response = client.post("/practice/events", json=payload)
        assert response.status_code == 200

    response = client.get("/practice/events")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get("/practice/insights/top-topics?k=2")
    assert response.status_code == 200
    assert response.json() == {"topics": ["arrays", "graphs"]}


def test_minutes_pair_success() -> None:
    client.post(
        "/practice/events",
        json={"topic": "arrays", "minutes": 45, "difficulty": "easy"},
    )
    client.post(
        "/practice/events",
        json={"topic": "graphs", "minutes": 30, "difficulty": "medium"},
    )

    response = client.get("/practice/insights/minutes-pair?target=75")
    assert response.status_code == 200
    assert response.json() == {"indices": [0, 1]}


def test_minutes_pair_not_found() -> None:
    client.post(
        "/practice/events",
        json={"topic": "arrays", "minutes": 45, "difficulty": "easy"},
    )

    response = client.get("/practice/insights/minutes-pair?target=999")
    assert response.status_code == 404


def test_minutes_pair_bad_request() -> None:
    response = client.get("/practice/insights/minutes-pair?target=0")
    assert response.status_code == 400
