from app.services.semantic_search_service import semantic_search


query = "highest paying jobs for software engineers"

results = semantic_search(
    query=query,
    top_k=3
)

print("\nQdrant Semantic Search Results:")

for rank, result in enumerate(results, start=1):

    print(
        f"\nRank {rank}"
    )

    print(
        "Similarity:",
        result["similarity"]
    )

    print(
        "Job:",
        result["job"]
    )