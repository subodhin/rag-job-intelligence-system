from app.context.database import initialize_database
from app.context.context_service import (
    save_message,
    get_conversation
)


initialize_database()

user_id = "user_001"


save_message(
    user_id,
    "user",
    "Find remote AI Engineer jobs."
)

save_message(
    user_id,
    "assistant",
    "I found several relevant AI Engineer jobs."
)

save_message(
    user_id,
    "user",
    "Only show jobs using Python."
)


print("Conversation:")
print(get_conversation(user_id))