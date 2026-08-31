from app.context.database import initialize_database
from app.context.context_service import create_user, get_user


initialize_database()

user_id = "user_001"

create_user(user_id)

user = get_user(user_id)

print("User:")
print(user)