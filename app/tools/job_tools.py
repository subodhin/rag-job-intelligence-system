from app.services.data_service import search_jobs_by_filters
from app.services.semantic_search_service import semantic_search


# Job search direct external api
def search_jobs_tool(filters):
    """
    Search jobs using structured filters.
    """
    return search_jobs_by_filters(filters)


def semantic_job_search_tool(query, top_k=3):
    """
    Search jobs using semantic similarity.
    """
    return semantic_search(query, top_k)