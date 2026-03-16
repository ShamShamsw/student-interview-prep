"""
operations.py - Core topic modeling workflow
===========================================

Contains data science logic only:
    - corpus preparation
    - vectorization
    - model fitting (NMF/LDA)
    - topic extraction
    - summary persistence
"""

from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from models import (
    create_document_topic,
    create_run_config,
    create_run_summary,
    create_topic,
)
from storage import save_latest_run


def load_sample_corpus() -> list[str]:
    """
    Return a built-in sample corpus for local runs.

    Returns:
        list[str]: Collection of short documents.
    """
    # TODO: Replace with file-based corpus loader when extending the project.
    return [
        "team won the game with strong defense and great scoring",
        "player scored a late goal in the final match",
        "coach discussed season strategy and training plans",
        "government passed a new policy about public education",
        "election debate focused on law and public rights",
        "senators discussed budget reform and tax policy",
        "model training improved accuracy on the dataset",
        "feature engineering helped classifier performance",
        "machine learning experiment used validation metrics",
        "company reported revenue growth and customer demand",
        "market trends impacted product pricing and sales",
        "startup focused on product strategy and retention",
    ]


def vectorize_corpus(corpus: list[str], max_features: int):
    """
    Vectorize text corpus into term-document matrix.

    Parameters:
        corpus (list[str]): Input documents.
        max_features (int): Vocabulary cap.

    Returns:
        tuple: (vectorizer, document_term_matrix)
    """
    # We suppress high-frequency terms and keep a compact vocabulary to
    # improve topic readability on small corpora.
    vectorizer = CountVectorizer(
        stop_words="english",
        max_df=0.95,
        min_df=1,
        max_features=max_features,
    )
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix


def extract_top_words(model, feature_names, top_n: int, model_name: str) -> list:
    """
    Extract top words per topic from a trained model.

    Parameters:
        model: Fitted NMF or LDA model.
        feature_names: Vocabulary list from vectorizer.
        top_n (int): Number of words to keep per topic.
        model_name (str): Label for output metadata.

    Returns:
        list[dict]: Topic summary entries.
    """
    topics = []
    for topic_id, topic_weights in enumerate(model.components_):
        top_indices = topic_weights.argsort()[-top_n:][::-1]
        words = [feature_names[i] for i in top_indices]
        topics.append(create_topic(topic_id, words, model_name))
    return topics


def get_dominant_topics(topic_distribution) -> list:
    """
    Compute dominant topic for each document.

    Parameters:
        topic_distribution: Doc-topic matrix from model.transform.

    Returns:
        list[dict]: Dominant topic entry per document.
    """
    dominant = []
    for idx, row in enumerate(topic_distribution):
        topic_id = int(row.argmax())
        dominant.append(create_document_topic(idx, topic_id, float(row[topic_id])))
    return dominant


def run_full_pipeline() -> dict:
    """
    Execute end-to-end topic modeling pipeline and persist run artifact.

    Returns:
        dict: Run summary object.
    """
    config = create_run_config()
    corpus = load_sample_corpus()

    vectorizer, matrix = vectorize_corpus(corpus, config["max_features"])
    features = vectorizer.get_feature_names_out()

    nmf_model = NMF(n_components=config["num_topics"], random_state=config["random_state"])
    nmf_doc_topics = nmf_model.fit_transform(matrix)

    lda_model = LatentDirichletAllocation(
        n_components=config["num_topics"],
        random_state=config["random_state"],
        learning_method="batch",
    )
    lda_doc_topics = lda_model.fit_transform(matrix)

    nmf_topics = extract_top_words(nmf_model, features, top_n=8, model_name="NMF")
    lda_topics = extract_top_words(lda_model, features, top_n=8, model_name="LDA")

    # Dominant topics are computed from LDA for probabilistic interpretation.
    dominant_topics = get_dominant_topics(lda_doc_topics)

    summary = create_run_summary(
        config=config,
        corpus_size=len(corpus),
        vocabulary_size=len(features),
        nmf_topics=nmf_topics,
        lda_topics=lda_topics,
        dominant_topics=dominant_topics,
    )
    save_latest_run(summary)
    return summary
