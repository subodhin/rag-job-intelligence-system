from app.services.data_service import search_jobs_by_filters
from app.services.semantic_search_service import semantic_search
from app.context.database import get_connection

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

# #agent workflow action
def save_job(user_id, job):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO job_tracking (
            user_id,
            job_id,
            title,
            job_url,
            status
        )
        VALUES (?, ?, ?, ?, 'saved')
    """, (
        user_id,
        str(job["id"]),
        job["title"],
        job["job_url"]
    ))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "action": "save_job",
        "job_id": job["id"],
        "title": job["title"],
        "status": "saved"
    }

def track_job(user_id, job_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE job_tracking
        SET status = ?,
            applied_at = CASE
                WHEN ? = 'applied' THEN CURRENT_TIMESTAMP
                ELSE applied_at
            END
        WHERE user_id = ?
          AND job_id = ?
    """, (
        status,
        status,
        user_id,
        str(job_id)
    ))

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return {
        "success": updated > 0,
        "action": "track_job",
        "job_id": job_id,
        "status": status
    }


def record_job_event(user_id, job_id, event_type):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO job_events (
            user_id,
            job_id,
            event_type
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        str(job_id),
        event_type
    ))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "event": event_type,
        "job_id": job_id
    }

def get_saved_jobs(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            job_id,
            title,
            job_url,
            status,
            saved_at,
            applied_at
        FROM job_tracking
        WHERE user_id = ?
        ORDER BY saved_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "job_id": row[0],
            "title": row[1],
            "job_url": row[2],
            "status": row[3],
            "saved_at": row[4],
            "applied_at": row[5]
        }
        for row in rows
    ]