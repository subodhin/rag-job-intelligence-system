from app.services.cv_graph import build_cv_graph


graph = build_cv_graph()


initial_state = {
    "cv_id": "cv_16caa1e9",
    "query": "How is the React experience?"
}


result = graph.invoke(initial_state)


print("\n========== FINAL GRAPH RESULT ==========")

print("CV ID:", result["cv_id"])
print("Query:", result["query"])
print("Results:", len(result["results"]))


for item in result["results"]:

    print("\nChunk:", item["chunk_index"])
    print("Score:", item["score"])
    print("Text:", item["text"][:300])


print("\n========== FINAL ANSWER ==========")
print(result["answer"])