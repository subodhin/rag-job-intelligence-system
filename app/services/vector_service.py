import faiss
import numpy as np


INDEX_PATH = "data/jobs.index"


def create_index(embedded_jobs):
    vectors = np.array(
        [job["embedding"] for job in embedded_jobs],
        dtype="float32"
    )

    # Normalize vectors for cosine similarity
    print("Vectors::::::::::::::::::::::::::", vectors)
    print("Vectors shape:::::::::::::::::::::::::::", vectors.shape)
    faiss.normalize_L2(vectors)

    dimension = vectors.shape[1]
    print("Dimension:::::::::::::::::::::::::::", dimension)

    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)
    print("iNDEX>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",index)

    return index


def save_index(index):
    faiss.write_index(index, INDEX_PATH)
    print(f"Index saved to: {INDEX_PATH}")