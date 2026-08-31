from app.context.database import initialize_database
from app.context.context_service import save_profile, get_profile


initialize_database()

user_id = "user_001"


print("Saving profile...")

save_profile(
    user_id=user_id,
    target_role="AI Engineer",
    experience_level="Senior",
    skills="Python, FastAPI, RAG"
)


print("\nProfile:")
print(get_profile(user_id))