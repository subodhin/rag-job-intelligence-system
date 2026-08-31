from app.context.database import initialize_database
from app.context.context_service import (
    save_preferences,
    get_preferences
)


initialize_database()

user_id = "user_001"


print("Saving preferences...")

save_preferences(
    user_id=user_id,
    remote_only=True,
    preferred_locations="Europe, Remote",
    preferred_skills="Python, RAG"
)


print("\nPreferences:")
print(get_preferences(user_id))