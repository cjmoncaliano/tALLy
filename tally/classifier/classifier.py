import pandas as pd
import numpy as np
import gensim
import sys

skills = ["leadership", "collaboration", "creativity", "quantitative", "adaptability", "persistence"]

def train_model(save_model = True):
    df = pd.read_csv('data/job_dataset_4_4.csv')
    df = df.dropna(subset=['RequiredQual'])
    job_requirements = df["RequiredQual"].tolist()

    processed_jobs = []
    for job in job_requirements:
        tokens = gensim.utils.simple_preprocess(job)
        processed_jobs.append(tokens)
    model = gensim.models.Word2Vec(
        processed_jobs,
        size=150,
        window=10,
        min_count=2,
        workers=3)
    model.train(processed_jobs, total_examples=len(processed_jobs), epochs=10)
    if save_model:
        model.save("models/word2vec.model")
    return model


def load_model(model_path):
    model = gensim.models.Word2Vec.load(model_path)
    return model

def return_skills():
    return skills

def score_experience(model, desc):
    desc = gensim.parsing.preprocessing.remove_stopwords(desc)
    desc = gensim.parsing.preprocessing.strip_numeric(desc)
    desc = gensim.parsing.preprocessing.strip_punctuation(desc)
    tokens = gensim.utils.simple_preprocess(desc)

    # order: leadership, collaborate, creativity, quantitative
    scores = [0, 0, 0, 0, 0, 0]
    for word in tokens:
        scores[0] += model.wv.similarity(word, "leadership")
        scores[1] += model.wv.similarity(word, "collaborate")
        scores[2] += model.wv.similarity(word, "creativity")
        scores[3] += model.wv.similarity(word, "math")
        scores[4] += model.wv.similarity(word, "adaptability")
        scores[5] += model.wv.similarity(word, "persistence")

    for ind in range(len(scores)):
        if scores[ind] < 0:
            scores[ind] = 0.0
    return scores
